"""Преобразование описаний устройств Zigbee2MQTT / Matter в типы и умения Яндекса."""

ZIGBEE_TYPES = {
    "light": "devices.types.light",
    "switch": "devices.types.switch",
    "plug": "devices.types.socket",
    "sensor": "devices.types.sensor",
}

MATTER_DEVICE_TYPES = {  # Matter Device Type ID -> тип Яндекса
    0x0100: "devices.types.light",    # On/Off Light
    0x010D: "devices.types.light",    # Extended Color Light
    0x010A: "devices.types.socket",   # On/Off Plug-in Unit
    0x0302: "devices.types.sensor",   # Temperature Sensor
}


def zigbee_to_yandex(dev: dict) -> dict:
    exposes = {e.get("type") for e in dev.get("definition", {}).get("exposes", [])}
    kind = "light" if "light" in exposes else "plug" if "switch" in exposes else "sensor"
    caps = [{"type": "devices.capabilities.on_off", "retrievable": True}] if kind != "sensor" else []
    return {"id": dev["ieee_address"], "name": dev.get("friendly_name", dev["ieee_address"]),
            "type": ZIGBEE_TYPES[kind], "capabilities": caps}


def matter_to_yandex(node_id: int, device_type: int, name: str) -> dict:
    ytype = MATTER_DEVICE_TYPES.get(device_type, "devices.types.other")
    caps = [] if ytype == "devices.types.sensor" else [{"type": "devices.capabilities.on_off", "retrievable": True}]
    return {"id": f"matter-{node_id}", "name": name, "type": ytype, "capabilities": caps}
