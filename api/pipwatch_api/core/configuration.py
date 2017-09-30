"""This module contains logic responsible for configuring flask-restplus application."""

from configparser import ConfigParser
from logging import config
from os import path
from typing import Dict, Optional

from celery import Celery  # noqa: F401 Imported for type definition
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from pipwatch_api.datastore.seed import seed_database

# Disable line too long warnings - configuration looks better in one line.
# pylint: disable=line-too-long

PATH_TO_DEFAULT_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config.ini")
PATH_TO_OVERRIDE_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config-override.ini")  # noqa: E501
PATH_TO_LOG_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "logging.conf")

CONFIGURATION_FILE: Optional[ConfigParser] = None


def load_config_file() -> ConfigParser:
    """Load configuration file into ConfigParser instance."""
    global CONFIGURATION_FILE  # pylint: disable=global-statement
    if not CONFIGURATION_FILE:
        CONFIGURATION_FILE = ConfigParser()
        CONFIGURATION_FILE.read([
            PATH_TO_DEFAULT_CONFIGURATION_FILE,
            PATH_TO_OVERRIDE_CONFIGURATION_FILE
        ], "utf-8")

    return CONFIGURATION_FILE


def configure_logger() -> None:
    """Apply settings from configuration file to loggers."""
    config.fileConfig(PATH_TO_LOG_CONFIGURATION_FILE)


def configure_celery_app(celery_app: Celery) -> None:
    """Apply configuration settings to celery application instance."""
    configuration: ConfigParser = load_config_file()
    celery_app.conf.update(
        broker_url=configuration.get(section="celery", option="broker_url", fallback="redis://localhost:6379/0"),  # noqa: E501
        enable_utc=configuration.getboolean(section="celery", option="enable_utc", fallback=True),  # noqa: E501
        imports=configuration.get(section="celery", option="imports", fallback="pipwatch_worker.celery_components.tasks").split(","),  # noqa: E501
        result_backend=configuration.get(section="celery", option="result_backend", fallback="redis://localhost:6379/0")  # noqa: E501
    )


def configure_sqlalchemy(application: Flask, sql_alchemy_instance: SQLAlchemy) -> None:
    """Initialize SQLAlchemy for flask application."""
    sql_alchemy_instance.init_app(app=application)

    with application.app_context():
        if application.config.get("PIPWATCH_API_RESET_DB_ON_START"):
            sql_alchemy_instance.drop_all()
            sql_alchemy_instance.create_all()
        if application.config.get("PIPWATCH_API_SEED_DB"):
            seed_database(database_instance=sql_alchemy_instance)


def configure_flask_application(application: Flask, settings_override: Dict = None) -> None:
    """Apply settings from configuration file to flask application instance."""
    configuration: ConfigParser = load_config_file()

    server_name = configuration.get(section="flask", option="server_name", fallback="")  # noqa: E501
    if server_name:
        application.config["SERVER_NAME"] = server_name

    application.config["DEBUG"] = configuration.getboolean(section="flask", option="debug", fallback=False)
    application.config["JSON_AS_ASCII"] = configuration.getboolean(section="flask", option="json_as_ascii", fallback=False)  # noqa: E501
    application.config["JSON_SORT_KEYS"] = configuration.getboolean(section="flask", option="json_sort_keys", fallback=True)  # noqa: E501

    application.config["RESTPLUS_ERROR_404_HELP "] = configuration.getboolean(section="flask-restplus", option="error_404_help", fallback=False)  # noqa: E501
    application.config["RESTPLUS_MASK_SWAGGER "] = configuration.getboolean(section="flask-restplus", option="mask_swagger", fallback=False)  # noqa: E501
    application.config["RESTPLUS_SWAGGER_UI_DOC_EXPANSION"] = configuration.get(section="flask-restplus", option="swagger_ui_doc_expansion", fallback="list")  # noqa: E501
    application.config["RESTPLUS_VALIDATE "] = configuration.getboolean(section="flask-restplus", option="validate", fallback=True)  # noqa: E501

    application.config["SQLALCHEMY_DATABASE_URI"] = configuration.get(section="sql-alchemy", option="database_uri", fallback="sqlite:////db.sqlite")  # noqa: E501
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = configuration.getboolean(section="sql-alchemy", option="track_modifications", fallback=False)  # noqa: E501

    application.config["PIPWATCH_API_HOST"] = configuration.get(section="pipwatch-api", option="host_address", fallback="127.0.0.1")  # noqa: E501
    application.config["PIPWATCH_API_PORT"] = configuration.getint(section="pipwatch-api", option="host_port", fallback=8080)  # noqa: E501

    application.config["PIPWATCH_API_RESET_DB_ON_START"] = configuration.getboolean(section="pipwatch-api", option="resest_db_on_start", fallback=True)  # noqa: E501
    application.config["PIPWATCH_API_SEED_DB"] = configuration.getboolean(section="pipwatch-api", option="seed_db", fallback=False)  # noqa: E501

    if not settings_override:
        return

    # Override any settings which were passed in explicitly
    for setting_key, setting_value in settings_override.items():
        application.config[setting_key] = setting_value
