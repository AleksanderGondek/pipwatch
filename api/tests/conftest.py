"""This module contains fixtures that are used throughout all the tests."""
import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest

from pipwatch_api.application import get_flask_application


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


@pytest.yield_fixture(scope="session")
def database(app) -> SQLAlchemy:
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
