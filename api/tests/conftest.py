"""This module contains fixtures that are used throughout all the tests."""
import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest

from pipwatch_api.application import get_flask_application

from tests.utils import JSONResponse


def get_test_database_path() -> str:
    """To be described."""
    test_suite_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(test_suite_dir, "testDb.sqlite")


@pytest.yield_fixture(scope="session")
def app() -> Flask:
    """Session-wide test instance of `Flask` application."""
    settings_override = {
        "DEBUG": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + get_test_database_path(),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "PIPWATCH_API_RESET_DB_ON_START": False,
        "PIPWATCH_API_SEED_DB": False
    }

    application = get_flask_application(settings_override=settings_override)
    context = application.app_context()
    context.push()

    yield application
    context.pop()


@pytest.fixture(scope="session")
def app_client(app) -> Flask:
    """Session-wide test instance of flask for testing resources."""
    app.testing = True
    app.response_class = JSONResponse
    return app.test_client()


@pytest.yield_fixture(scope="session")
def database_session_wide(app) -> SQLAlchemy:
    """Session-wide test instance of database."""
    if os.path.exists(get_test_database_path()):
        os.unlink(get_test_database_path())

    from pipwatch_api.datastore.models import DATABASE
    DATABASE.init_app(app=app)
    DATABASE.create_all()
    yield DATABASE

    DATABASE.drop_all()
    DATABASE.session.close()

    os.unlink(get_test_database_path())


@pytest.yield_fixture()
def database(database_session_wide, mocker) -> SQLAlchemy:
    """Database instance which mocks commits and rollbacks all changes."""
    mocker.patch.object(database_session_wide.session, "commit", autospec=True)
    yield database_session_wide

    database_session_wide.session.rollback()
