from fastapi.testclient import TestClient

from cloud.app.main import app

c = TestClient(app)
H = {"Authorization": "Bearer test-token", "X-Request-Id": "r1"}


def test_ping():
    assert c.head("/v1.0/").status_code == 200


def test_unauthorized():
    assert c.get("/v1.0/user/devices").status_code == 401


def test_discovery():
    r = c.get("/v1.0/user/devices", headers=H).json()
    assert r["request_id"] == "r1"
    assert {d["id"] for d in r["payload"]["devices"]} == {"lamp-1", "socket-1"}


def test_action_then_query():
    body = {"payload": {"devices": [{"id": "lamp-1", "capabilities": [
        {"type": "devices.capabilities.on_off", "state": {"instance": "on", "value": True}}]}]}}
    r = c.post("/v1.0/user/devices/action", json=body, headers=H).json()
    assert r["payload"]["devices"][0]["capabilities"][0]["state"]["action_result"]["status"] == "DONE"
    q = c.post("/v1.0/user/devices/query", json={"devices": [{"id": "lamp-1"}]}, headers=H).json()
    assert q["payload"]["devices"][0]["capabilities"][0]["state"]["value"] is True


def test_unknown_device():
    q = c.post("/v1.0/user/devices/query", json={"devices": [{"id": "x"}]}, headers=H).json()
    assert q["payload"]["devices"][0]["error_code"] == "DEVICE_NOT_FOUND"
    

def test_query_several_devices():
    body = {"devices": [{"id": "socket-1"}, {"id": "lamp-1"}, {"id": "nope"}]}
    q = c.post("/v1.0/user/devices/query", json=body, headers=H).json()
    devices = q["payload"]["devices"]
    assert [d["id"] for d in devices] == ["socket-1", "lamp-1", "nope"]
    socket_state = devices[0]["capabilities"][0]
    assert socket_state["type"] == "devices.capabilities.on_off"
    assert socket_state["state"] == {"instance": "on", "value": True}
    assert devices[2]["error_code"] == "DEVICE_NOT_FOUND"

    

def test_unlink():
    r = c.post("/v1.0/user/unlink", headers=H)
    assert r.status_code == 200
    assert r.json()["request_id"] == "r1"


def test_action_unknown_device():
    body = {"payload": {"devices": [{"id": "x", "capabilities": [
        {"type": "devices.capabilities.on_off", "state": {"instance": "on", "value": True}}]}]}}
    r = c.post("/v1.0/user/devices/action", json=body, headers=H).json()
    result = r["payload"]["devices"][0]["capabilities"][0]["state"]["action_result"]
    assert result["status"] == "ERROR"
    assert result["error_code"] == "DEVICE_NOT_FOUND"
