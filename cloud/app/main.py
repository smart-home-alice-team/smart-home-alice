"""Адаптер навыка умного дома: протокол платформы Yandex Smart Home (REST, /v1.0)."""
from fastapi import FastAPI, Header, HTTPException, Request, Response

from .devices import DEVICES, capability_states

app = FastAPI(title="Smart Home Alice Skill")
TEST_TOKEN = "test-token"  # в рабочей версии проверяется токен OAuth 2.0


def auth(authorization: str | None) -> str:
    if authorization != f"Bearer {TEST_TOKEN}":
        raise HTTPException(status_code=401)
    return "user-1"


@app.head("/v1.0/")
def ping() -> Response:
    return Response(status_code=200)


@app.post("/v1.0/user/unlink")
def unlink(x_request_id: str = Header(""), authorization: str | None = Header(None)):
    auth(authorization)
    return {"request_id": x_request_id}


@app.get("/v1.0/user/devices")
def devices(x_request_id: str = Header(""), authorization: str | None = Header(None)):
    user = auth(authorization)
    items = [{k: v for k, v in d.items() if k != "state"} for d in DEVICES.values()]
    return {"request_id": x_request_id, "payload": {"user_id": user, "devices": items}}


@app.post("/v1.0/user/devices/query")
async def query(request: Request, x_request_id: str = Header(""), authorization: str | None = Header(None)):
    auth(authorization)
    body = await request.json()
    out = []
    for item in body.get("devices", []):
        d = DEVICES.get(item["id"])
        if d is None:
            out.append({"id": item["id"], "error_code": "DEVICE_NOT_FOUND"})
            continue
        out.append({"id": d["id"], "capabilities": capability_states(d)})
    return {"request_id": x_request_id, "payload": {"devices": out}}


@app.post("/v1.0/user/devices/action")
async def action(request: Request, x_request_id: str = Header(""), authorization: str | None = Header(None)):
    auth(authorization)
    body = await request.json()
    out = []
    for item in body["payload"]["devices"]:
        d = DEVICES.get(item["id"])
        caps = []
        for cap in item["capabilities"]:
            if d is None:
                caps.append({"type": cap["type"], "state": {"instance": cap["state"]["instance"],
                             "action_result": {"status": "ERROR", "error_code": "DEVICE_NOT_FOUND"}}})
                continue
            d["state"]["on"] = bool(cap["state"]["value"])  # в рабочей версии — команда шлюзу через MQTT
            caps.append({"type": cap["type"], "state": {"instance": "on", "action_result": {"status": "DONE"}}})
        out.append({"id": item["id"], "capabilities": caps})
    return {"request_id": x_request_id, "payload": {"devices": out}}
