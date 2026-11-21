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


def test_zigbee_switch_is_socket():
    dev = {"ieee_address": "0x3", "friendly_name": "Розетка",
           "definition": {"exposes": [{"type": "switch"}]}}
    d = zigbee_to_yandex(dev)
    assert d["type"] == "devices.types.socket"
    assert d["capabilities"][0]["type"] == "devices.capabilities.on_off"


def test_zigbee_name_defaults_to_address():
    dev = {"ieee_address": "0x4", "definition": {"exposes": [{"type": "light"}]}}
    assert zigbee_to_yandex(dev)["name"] == "0x4"


def test_matter_unknown_type_is_other():
    d = matter_to_yandex(7, 0xFFFF, "Неизвестное")
    assert d["type"] == "devices.types.other"
    assert d["capabilities"][0]["type"] == "devices.capabilities.on_off"


def test_matter_temperature_sensor_has_no_capabilities():
    assert matter_to_yandex(8, 0x0302, "Термометр")["capabilities"] == []