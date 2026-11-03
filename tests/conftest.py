import pytest

from main import create_app


@pytest.fixture
def app(tmp_path):
    """Application de test avec une base SQLite temporaire (CSRF désactivé)."""
    return create_app("testing", {"DATABASE": str(tmp_path / "test.db")})


@pytest.fixture
def client(app):
    return app.test_client()
