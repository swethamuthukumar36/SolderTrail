import psycopg

import app.main as main
from app.config import Settings, get_settings


def test_health_is_fast_and_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {
        "status": "ok",
        "app": "examate-rag",
        "environment": "test",
    }


def test_ready_without_database(client):
    r = client.get("/ready")

    assert r.status_code == 200
    assert r.json() == {
        "status": "ok",
        "database": "not configured",
    }


def test_ready_when_database_is_unavailable(client, monkeypatch):
    def failed_connection(*args, **kwargs):
        raise psycopg.OperationalError("Database unavailable")

    monkeypatch.setattr(main.psycopg, "connect", failed_connection)

    app_settings = Settings(
        app_name="examate-rag",
        environment="test",
        database_url="postgresql://test:test@localhost:5432/test",
    )

    main.app.dependency_overrides[get_settings] = lambda: app_settings

    r = client.get("/ready")

    assert r.status_code == 503
    assert r.json() == {
        "status": "not_ready",
        "database": "unavailable",
    }
