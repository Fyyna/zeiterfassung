"""
Gemeinsame Test-Hilfen (Fixtures).

Ein Test bekommt eine Fixture, indem er sie als Parameter verlangt:
    def test_etwas(client): ...
Jeder Test bekommt eine eigene, frisch angelegte Datenbank.
"""

import pytest

import db
from app import app as flask_app


@pytest.fixture
def app(tmp_path):
    flask_app.config.update(DATABASE=str(tmp_path / "test.sqlite"), TESTING=True)
    with flask_app.app_context():
        db.tabellen_anlegen()
    return flask_app


@pytest.fixture
def client(app):
    """Ein Test-Browser, der Seiten aufrufen und Formulare abschicken kann."""
    return app.test_client()
