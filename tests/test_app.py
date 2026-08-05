import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.app import app


def client():
    return app.test_client()


def test_index_ok():
    resp = client().get("/")
    assert resp.status_code == 200
    assert b"Client Info Echo" in resp.data


def test_healthz_ok():
    resp = client().get("/healthz")
    assert resp.status_code == 200
    assert resp.data == b"ok"


def test_api_whoami_reports_headers_and_cookies():
    resp = client().get(
        "/api/whoami",
        headers={"X-Test-Header": "hello"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["headers"]["X-Test-Header"] == "hello"
    assert "ip" in data
    assert "cookies" in data


def test_set_cookie_roundtrip():
    c = client()
    c.set_cookie("f5_demo_cookie", "abc123")
    resp = c.get("/api/whoami")
    data = resp.get_json()
    assert data["cookies"].get("f5_demo_cookie") == "abc123"
