"""Агент шлюза: связывает Zigbee2MQTT и Matter-контроллер с облачным сервисом по MQTT/TLS."""
import os


def main() -> None:
    host = os.getenv("MQTT_HOST", "localhost")
    print(f"gateway agent: connecting to {host} (каркас; реализация — задачи A18–A21)")


if __name__ == "__main__":
    main()
