"""This package contains logic responsible for creating database and representing data objects."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DATABASE = SQLAlchemy()


def initialize_database(application: Flask) -> None:
    """Initialize SQLAlchemy for flask application."""
    DATABASE.init_app(app=application)
    if not application.config.get("PIPWATCHAPI_RESET_DB_ON_START"):
        return

    from pipwatch_api.datastore.models import Project  # noqa: F401
    with application.app_context():
        DATABASE.drop_all()
        DATABASE.create_all()
