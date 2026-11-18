# Навык умного дома для Яндекс Алисы (Zigbee / Matter)

Учебный проект по дисциплине «Управление программными проектами».
Команда: Карина (руководитель проекта, аналитик, тестирование), Илья (облачный сервис навыка), Алексей (ПО шлюза, Zigbee/Matter, DevOps).

## Состав
| Каталог | Назначение |
|---|---|
| `cloud/` | Облачный адаптер навыка: протокол Yandex Smart Home (`/v1.0/...`), OAuth 2.0, веб-кабинет (FastAPI) |
| `gateway/` | Агент локального шлюза: Zigbee2MQTT, Matter-контроллер, MQTT/TLS-канал в облако |
| `infra/` | Конфигурация Mosquitto и Zigbee2MQTT для Docker Compose |
| `docs/` | Проектная документация (требования, архитектура, протоколы встреч, журнал изменений) |
| `project/` | Задачи проекта (WBS) для импорта в трекер |

## Быстрый старт
```bash
cp .env.example .env
docker compose up -d --build        # облако + брокер + БД
docker compose --profile gateway up -d   # на Raspberry Pi: шлюз, Zigbee2MQTT, Matter
```
Проверка: `curl -I http://localhost:8000/v1.0/` → `200 OK`.

## Тесты
```bash
pip install -r cloud/requirements.txt -r gateway/requirements.txt
pytest -q
```

## Правила работы
См. [CONTRIBUTING.md](CONTRIBUTING.md).

## Как развернуть рабочее пространство команды
1. Создать организацию или репозиторий на GitHub, загрузить этот каталог:
   `git init && git add . && git commit -m "chore: каркас проекта" && git branch -M main && git remote add origin <url> && git push -u origin main`,
   затем создать ветку `develop`.
2. Settings → Collaborators: пригласить участников с ролями из CONTRIBUTING.md; Branches → защитить `main` и `develop` (только PR, 1 одобрение, зелёный CI).
3. Projects → New project (Board): колонки Backlog / To Do / In Progress / Review / Done; поля «Код WBS», «Оценка», «Итерация», «Приоритет».
4. Создать задачи из `project/tasks.csv` (37 работ WBS) и назначить исполнителей.
5. Включить Wiki для протоколов встреч и решений (шаблон — `docs/meeting-template.md`).
