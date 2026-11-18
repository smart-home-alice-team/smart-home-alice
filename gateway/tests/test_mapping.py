from gateway.agent.mapping import matter_to_yandex, zigbee_to_yandex


def test_zigbee_light():
    dev = {"ieee_address": "0x00158d0001", "friendly_name": "Лампа",
           "definition": {"exposes": [{"type": "light"}]}}
    assert zigbee_to_yandex(dev)["type"] == "devices.types.light"


def test_zigbee_sensor_has_no_on_off():
    dev = {"ieee_address": "0x2", "definition": {"exposes": [{"type": "numeric"}]}}
    assert zigbee_to_yandex(dev)["capabilities"] == []


def test_matter_plug():
    d = matter_to_yandex(5, 0x010A, "Розетка")
    assert d["id"] == "matter-5" and d["type"] == "devices.types.socket"
