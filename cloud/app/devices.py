"""Реестр устройств пользователя (заглушка; в рабочей версии — PostgreSQL + Redis)."""
DEVICES = {
    "lamp-1": {
        "id": "lamp-1", "name": "Лампа", "room": "Гостиная",
        "type": "devices.types.light",
        "capabilities": [{"type": "devices.capabilities.on_off", "retrievable": True}],
        "device_info": {"manufacturer": "Zigbee", "model": "TS0505B"},
        "state": {"on": False},
    },
    "socket-1": {
        "id": "socket-1", "name": "Розетка", "room": "Кухня",
        "type": "devices.types.socket",
        "capabilities": [{"type": "devices.capabilities.on_off", "retrievable": True}],
        "device_info": {"manufacturer": "Matter", "model": "Smart Plug"},
        "state": {"on": True},
    },
}
