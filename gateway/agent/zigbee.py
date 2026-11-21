"""Обмен сообщениями с Zigbee2MQTT: список устройств, состояния и команды."""
import json

from .mapping import zigbee_to_yandex

BASE_TOPIC = "zigbee2mqtt"


def parse_devices(payload: str) -> list[dict]:
    """Топик zigbee2mqtt/bridge/devices -> список устройств в формате Яндекса."""
    devices = json.loads(payload)
    return [zigbee_to_yandex(d) for d in devices if d.get("type") != "Coordinator"]


def parse_state(payload: str) -> bool | None:
    """Топик zigbee2mqtt/<имя>: True - включено, False - выключено, None - нет данных."""
    state = json.loads(payload).get("state")
    if state is None:
        return None
    return str(state).upper() == "ON"


def build_command(friendly_name: str, on: bool) -> tuple[str, str]:
    """Команда вкл/выкл: (топик, текст сообщения) для Zigbee2MQTT."""
    topic = f"{BASE_TOPIC}/{friendly_name}/set"
    return topic, json.dumps({"state": "ON" if on else "OFF"})