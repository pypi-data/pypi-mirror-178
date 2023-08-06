# See:
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf
# https://app-h5.govee.com/user-manual/wlan-guide

import asyncio
from copy import copy, deepcopy
from dataclasses import dataclass
import json
import logging
import socket
import ssl
from typing import Any, Callable, Dict, List, Optional, Tuple

import aiohttp
import certifi

BROADCAST_PORT = 4001
COMMAND_PORT = 4003
LISTEN_PORT = 4002
BROADCAST_ADDR = "239.255.255.250"

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoveeColor:
    red: int = 0
    green: int = 0
    blue: int = 0

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def as_json_object(self) -> Dict[str, int]:
        return {"r": self.red, "g": self.green, "b": self.blue}


@dataclass
class GoveeDeviceState:
    turned_on: bool = False
    brightness_pct: int = 0
    color: Optional[GoveeColor] = None
    color_temperature: Optional[int] = None

    def __repr__(self):
        return str(self.__dict__)


@dataclass
class GoveeHttpDeviceDefinition:
    device_id: str
    model: str
    device_name: str
    controllable: bool
    retrievable: bool
    supported_commands: List[str]
    properties: Dict[str, Any]


async def _extract_failure_message(response) -> str:
    try:
        data = await response.json()
        if "message" in data:
            return data["message"]
    except Exception:  # pylint: disable=broad-except
        pass
    return await response.text()


async def http_get_devices(api_key: str) -> List[GoveeHttpDeviceDefinition]:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    message = "Failed for an unknown reason"
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(
            url="https://developer-api.govee.com/v1/devices",
            headers={"Govee-API-Key": api_key},
        ) as response:
            if response.status == 200:
                data = await response.json()
                if (
                    ("data" in data)
                    and ("devices" in data["data"])
                    and isinstance(data["data"]["devices"], list)
                ):
                    return [
                        GoveeHttpDeviceDefinition(
                            device_id=d["device"],
                            model=d["model"],
                            device_name=d["deviceName"],
                            controllable=d["controllable"],
                            retrievable=d["retrievable"],
                            supported_commands=d["supportCmds"],
                            properties=d["properties"],
                        )
                        for d in data["data"]["devices"]
                    ]

            message = await _extract_failure_message(response)
    raise RuntimeError(f"failed to get devices: {message}")


async def http_get_state(api_key: str, device_id: str, model: str) -> List[Any]:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    message = "Failed for an unknown reason"
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(
            url="https://developer-api.govee.com/v1/devices/state",
            headers={"Govee-API-Key": api_key},
            params={"model": model, "device": device_id},
        ) as response:
            if response.status == 200:
                data = await response.json()
                if "data" in data and "properties" in data["data"]:
                    return data["data"]["properties"]

            message = await _extract_failure_message(response)
    raise RuntimeError(f"failed to get device state: {message}")


async def http_device_control(api_key: str, params: Dict[str, Any]):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    message = "Failed for an unknown reason"
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.put(
            url="https://developer-api.govee.com/v1/devices/control",
            headers={"Govee-API-Key": api_key},
            json=params,
        ) as response:
            if response.status == 200:
                resp = await response.json()
                return resp
            message = await _extract_failure_message(response)
    raise RuntimeError(f"failed to control device: {message}")


@dataclass
class GoveeLanDeviceDefinition:
    ip_addr: str
    device_id: str
    model: str
    ble_hardware_version: str
    ble_software_version: str
    wifi_hardware_version: str
    wifi_software_version: str


class GoveeDevice:
    state: Optional[GoveeDeviceState] = None
    http_definition: Optional[GoveeHttpDeviceDefinition] = None
    lan_definition: Optional[GoveeLanDeviceDefinition] = None
    device_id: str
    model: str

    def __init__(self, device_id: str, model: str):
        self.device_id = device_id
        self.model = model

    def __repr__(self):
        return str(self.__dict__)


# Type for device changed event callback
DeviceUpdated = Callable[[GoveeDevice], None]


class GoveeController:
    api_key: Optional[str] = None
    on_device_changed: Optional[DeviceUpdated] = None
    http_poller: Optional[asyncio.Task] = None
    lan_pollers: List[asyncio.Task]
    http_devices: Dict[str, GoveeHttpDeviceDefinition]
    devices: Dict[str, GoveeDevice]
    waiting_for_status: Dict[str, List[asyncio.Future]]
    device_control_timeout: int = 10

    def __init__(self):
        self.http_devices = {}
        self.lan_pollers = []
        self.devices = {}
        self.waiting_for_status = {}

    def set_http_api_key(self, api_key: str):
        """Sets the API for use with the HTTP API"""
        self.api_key = api_key

    def set_device_control_timeout(self, timeout: int):
        self.device_control_timeout = timeout

    def set_device_change_callback(self, on_change: DeviceUpdated):
        self.on_device_changed = on_change

    def start_lan_poller(
        self, interfaces: Optional[List[str]] = None, interval: float = 10
    ):
        if self.lan_pollers:
            raise RuntimeError("lan poller is already running")

        interfaces = interfaces or ["0.0.0.0"]
        for iface in interfaces:
            self.lan_pollers.append(
                asyncio.create_task(self._lan_poller(iface, interval))
            )

    def start_http_poller(self, interval: int):
        if self.api_key is None:
            raise RuntimeError("api_key is required to use the HTTP api")
        if self.http_poller:
            raise RuntimeError("http poller is already running")
        self.http_poller = asyncio.create_task(self._http_poller(interval))

    async def query_http_devices(self) -> List[GoveeHttpDeviceDefinition]:
        """Make an immediate call to the HTTP API to list available devices"""
        if self.api_key is None:
            raise RuntimeError("api_key is required to use the HTTP api")
        devices = await http_get_devices(self.api_key)
        self.http_devices = {dev.device_id: dev for dev in devices}

        for definition in devices:
            if dev := self.devices.get(definition.device_id, None):
                dev.http_definition = definition
            else:
                # Newly discovered
                dev = GoveeDevice(definition.device_id, definition.model)
                dev.http_definition = definition
                self.devices[dev.device_id] = dev
                self._fire_device_change(dev)

        return devices

    def get_device_by_id(self, device_id: str) -> Optional[GoveeDevice]:
        return self.devices.get(device_id, None)

    def _send_lan_command(self, lan_definition: GoveeLanDeviceDefinition, cmd: Any):
        data = bytes(json.dumps(cmd), "utf-8")
        dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dgram_socket.sendto(data, (lan_definition.ip_addr, COMMAND_PORT))

    def _request_lan_status(self, lan_definition: GoveeLanDeviceDefinition):
        self._send_lan_command(
            lan_definition,
            {
                "msg": {
                    "cmd": "devStatus",
                    "data": {},
                }
            },
        )

    def _complete_lan_futures(self, device: GoveeDevice):
        if futures := self.waiting_for_status.get(device.device_id, None):
            futures_copied = copy(futures)
            for future in futures_copied:
                if not future.cancelled():
                    future.set_result(None)
                futures.remove(future)

    async def update_device_state(self, device: GoveeDevice) -> GoveeDeviceState:
        """Fetches the current state of device, updating its state
        property and triggering the device changed event if
        appropriate"""

        if device.lan_definition:
            future = asyncio.get_event_loop().create_future()
            try:
                if device.device_id not in self.waiting_for_status:
                    self.waiting_for_status[device.device_id] = []
                self.waiting_for_status[device.device_id].append(future)
                self._request_lan_status(device.lan_definition)
                await asyncio.wait_for(future, timeout=self.device_control_timeout)
                assert device.state is not None
                return device.state

            finally:
                try:
                    self.waiting_for_status[device.device_id].remove(future)
                except ValueError:
                    pass

        if self.api_key:
            properties = await asyncio.wait_for(
                http_get_state(self.api_key, device.device_id, device.model),
                timeout=self.device_control_timeout,
            )

            turned_on = False
            brightness_pct = 100
            color: Optional[GoveeColor] = None
            color_temperature: Optional[int] = None

            for prop in properties:
                if "powerState" in prop:
                    turned_on = prop["powerState"] == "on"
                if "brightness" in prop:
                    brightness_pct = prop["brightness"]
                if "color" in prop:
                    color = GoveeColor(
                        red=prop["color"]["r"],
                        green=prop["color"]["g"],
                        blue=prop["color"]["b"],
                    )
                if "colorTem" in prop:
                    color_temperature = (
                        None if prop["colorTem"] == 0 else prop["colorTem"]
                    )

            state = GoveeDeviceState(
                turned_on, brightness_pct, color, color_temperature
            )
            changed = state != device.state
            if changed:
                device.state = state
                self._fire_device_change(device)
            assert device.state is not None
            return device.state

        raise RuntimeError("either call start_lan_poller or set_http_api_key")

    async def set_power_state(self, device: GoveeDevice, turned_on: bool):
        if device.lan_definition:
            self._send_lan_command(
                device.lan_definition,
                {
                    "msg": {
                        "cmd": "turn",
                        "data": {"value": 1 if turned_on else 0},
                    }
                },
            )
            await self.update_device_state(device)
            return

        if self.api_key and device.http_definition:
            if "turn" not in device.http_definition.supported_commands:
                raise RuntimeError("device doesn't support turn command")

            assumed_state = deepcopy(
                device.state
                or GoveeDeviceState(
                    turned_on=True, brightness_pct=0, color=None, color_temperature=None
                )
            )
            assumed_state.turned_on = turned_on
            await asyncio.wait_for(
                http_device_control(
                    self.api_key,
                    {
                        "device": device.device_id,
                        "model": device.model,
                        "cmd": {
                            "name": "turn",
                            "value": "on" if turned_on else "off",
                        },
                    },
                ),
                timeout=self.device_control_timeout,
            )
            device.state = assumed_state
            return

        raise RuntimeError("either call start_lan_poller or set_http_api_key")

    async def set_color(self, device: GoveeDevice, color: GoveeColor):
        if device.lan_definition:
            self._send_lan_command(
                device.lan_definition,
                {
                    "msg": {
                        "cmd": "colorwc",
                        "data": {
                            "color": color.as_json_object(),
                        },
                    }
                },
            )
            await self.update_device_state(device)
            return

        if self.api_key and device.http_definition:
            if "color" not in device.http_definition.supported_commands:
                raise RuntimeError("device doesn't support color command")

            assumed_state = deepcopy(
                device.state
                or GoveeDeviceState(
                    turned_on=True,
                    brightness_pct=100,
                    color=None,
                    color_temperature=None,
                )
            )
            assumed_state.turned_on = True
            assumed_state.color = color
            assumed_state.color_temperature = None

            await asyncio.wait_for(
                http_device_control(
                    self.api_key,
                    {
                        "device": device.device_id,
                        "model": device.model,
                        "cmd": {
                            "name": "color",
                            "value": color.as_json_object(),
                        },
                    },
                ),
                timeout=self.device_control_timeout,
            )
            device.state = assumed_state
            return

        raise RuntimeError("either call start_lan_poller or set_http_api_key")

    async def set_color_temperature(self, device: GoveeDevice, color_temperature: int):
        if device.lan_definition:
            self._send_lan_command(
                device.lan_definition,
                {
                    "msg": {
                        "cmd": "colorwc",
                        "data": {
                            "colorTemInKelvin": color_temperature,
                        },
                    }
                },
            )
            await self.update_device_state(device)
            return

        if self.api_key and device.http_definition:
            if "colorTem" not in device.http_definition.supported_commands:
                raise RuntimeError("device doesn't support colorTem command")

            assumed_state = deepcopy(
                device.state
                or GoveeDeviceState(
                    turned_on=True,
                    brightness_pct=100,
                    color=None,
                    color_temperature=None,
                )
            )
            assumed_state.turned_on = True
            assumed_state.color = None
            assumed_state.color_temperature = color_temperature

            await asyncio.wait_for(
                http_device_control(
                    self.api_key,
                    {
                        "device": device.device_id,
                        "model": device.model,
                        "cmd": {
                            "name": "colorTem",
                            "value": color_temperature,
                        },
                    },
                ),
                timeout=self.device_control_timeout,
            )
            device.state = assumed_state
            return

        raise RuntimeError("either call start_lan_poller or set_http_api_key")

    async def set_brightness(self, device: GoveeDevice, brightness_pct: int):
        if device.lan_definition:
            self._send_lan_command(
                device.lan_definition,
                {
                    "msg": {
                        "cmd": "brightness",
                        "data": {"value": brightness_pct},
                    }
                },
            )
            await self.update_device_state(device)
            return

        if self.api_key and device.http_definition:
            if "brightness" not in device.http_definition.supported_commands:
                raise RuntimeError("device doesn't support brightness command")

            assumed_state = deepcopy(
                device.state
                or GoveeDeviceState(
                    turned_on=True,
                    brightness_pct=100,
                    color=None,
                    color_temperature=None,
                )
            )
            assumed_state.turned_on = True
            assumed_state.brightness_pct = brightness_pct

            await asyncio.wait_for(
                http_device_control(
                    self.api_key,
                    {
                        "device": device.device_id,
                        "model": device.model,
                        "cmd": {
                            "name": "brightness",
                            "value": brightness_pct,
                        },
                    },
                ),
                timeout=self.device_control_timeout,
            )
            device.state = assumed_state
            return
        raise RuntimeError("either call start_lan_poller or set_http_api_key")

    async def _http_poller(self, interval: int):
        while True:
            await self.query_http_devices()
            await asyncio.sleep(interval)

    async def _lan_poller(self, interface, interval: float):
        loop = asyncio.get_event_loop()
        transport, _protocol = await loop.create_datagram_endpoint(
            lambda: GoveeLanListener(self), local_addr=(interface, LISTEN_PORT)
        )
        try:
            mcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mcast.setsockopt(
                socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface)
            )
            mcast.setsockopt(
                socket.SOL_IP,
                socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(BROADCAST_ADDR) + socket.inet_aton(interface),
            )
            mcast.bind((interface, 0))

            while True:
                mcast.sendto(
                    b'{"msg":{"cmd":"scan","data":{"account_topic":"reserve"}}}',
                    (BROADCAST_ADDR, BROADCAST_PORT),
                )
                await asyncio.sleep(interval)

        finally:
            transport.close()

    def _lan_poller_process_broadcast(self, msg: Dict[str, Any], addr: str):
        source_ip = addr[0]
        msg = msg["msg"]
        data = msg["data"]
        if msg["cmd"] == "scan":
            device = GoveeDevice(device_id=data["device"], model=data["sku"])
            device.lan_definition = GoveeLanDeviceDefinition(
                ip_addr=data["ip"],
                device_id=data["device"],
                model=data["sku"],
                ble_hardware_version=data["bleVersionHard"],
                ble_software_version=data["bleVersionSoft"],
                wifi_hardware_version=data["wifiVersionHard"],
                wifi_software_version=data["wifiVersionSoft"],
            )

            if existing := self.devices.get(device.device_id, None):
                changed = existing.lan_definition != device.lan_definition
                if changed:
                    existing.lan_definition = device.lan_definition
                    self._fire_device_change(existing)
            else:
                # Newly discovered
                self.devices[device.device_id] = device
                self._fire_device_change(device)

            return

        if msg["cmd"] == "devStatus":
            color = None
            if rgb := data.get("color", None):
                color = GoveeColor(
                    red=rgb["r"],
                    green=rgb["g"],
                    blue=rgb["b"],
                )
            state = GoveeDeviceState(
                turned_on=data["onOff"] == 1,
                brightness_pct=data["brightness"],
                color=color,
                color_temperature=data.get("colorTemInKelvin", None),
            )
            for device in self.devices.values():
                if lan := device.lan_definition:
                    if lan.ip_addr == source_ip:
                        changed = device.state != state
                        if changed:
                            device.state = state
                            self._fire_device_change(device)

                        self._complete_lan_futures(device)
                        return

            _LOGGER.warning(
                "datagram_received: didn't find device for %r from %s %r",
                msg,
                addr,
                state,
            )
            return

        _LOGGER.warning("unknown msg: %r from %s", msg, addr)

    def _fire_device_change(self, device: GoveeDevice):
        if self.on_device_changed:
            self.on_device_changed(device)

    def stop(self):
        if self.http_poller:
            self.http_poller.cancel()
            self.http_poller = None
        for task in self.lan_pollers:
            task.cancel()
        self.lan_pollers = []


class GoveeLanListener(asyncio.DatagramProtocol):
    transport = None

    def __init__(self, controller: GoveeController):
        self.controller = controller

    def connection_lost(self, exc):
        pass

    def connection_made(self, transport):
        self.transport = transport

    # pylint: disable=protected-access
    def datagram_received(self, data, addr):
        message = data.decode()
        msg = json.loads(message)
        self.controller._lan_poller_process_broadcast(msg, addr)
