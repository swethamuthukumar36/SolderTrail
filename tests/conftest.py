import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app


@pytest.fixture
def client():
    settings = Settings(
        app_name="examate-rag",
        environment="test",
        database_url="",
    )

    app.dependency_overrides[get_settings] = lambda: settings

    with TestClient(app) as c:
        c.settings = settings
        yield c

    app.dependency_overrides.clear()