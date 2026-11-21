import json

from gateway.agent.zigbee import build_command, parse_devices, parse_state


def test_parse_devices_skips_coordinator():
    payload = json.dumps([
        {"ieee_address": "0x00", "type": "Coordinator"},
        {"ieee_address": "0x01", "type": "Router", "friendly_name": "Лампа",
         "definition": {"exposes": [{"type": "light"}]}},
    ])
    devices = parse_devices(payload)
    assert len(devices) == 1
    assert devices[0]["type"] == "devices.types.light"
    assert devices[0]["name"] == "Лампа"


def test_parse_state():
    assert parse_state('{"state": "ON", "brightness": 120}') is True
    assert parse_state('{"state": "OFF"}') is False
    assert parse_state('{"temperature": 21.5}') is None


def test_build_command():
    topic, payload = build_command("Лампа", True)
    assert topic == "zigbee2mqtt/Лампа/set"
    assert json.loads(payload) == {"state": "ON"}