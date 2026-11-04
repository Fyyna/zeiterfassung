"""
Shared test helpers (fixtures).

A test gets a fixture by asking for it as a parameter:
    def test_something(client): ...
Every test gets its own, fresh database.
"""

import pytest

from app import app as flask_app


@pytest.fixture
def app(tmp_path):
    # tmp_path is a new empty folder for every test -> fresh database every time.
    # DB_HANDLER creates the tables automatically on first use.
    flask_app.config.update(DATABASE=str(tmp_path / "test.sqlite"), TESTING=True)
    return flask_app


@pytest.fixture
def client(app):
    """A test browser that can open pages and submit forms."""
    return app.test_client()