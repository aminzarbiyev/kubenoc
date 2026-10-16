from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_status(monkeypatch):
    monkeypatch.setattr(main, "fetch_probes", lambda: [
        {"metric": {"instance": "8.8.8.8"}, "value": [0, "1"]},
        {"metric": {"instance": "10.0.0.1"}, "value": [0, "0"]},
    ])
    d = client.get("/status").json()
    assert d["total"] == 2 and d["up"] == 1 and d["down_targets"] == ["10.0.0.1"]


def test_status_prom_down(monkeypatch):
    def boom():
        raise RuntimeError("x")
    monkeypatch.setattr(main, "fetch_probes", boom)
    assert client.get("/status").status_code == 502
