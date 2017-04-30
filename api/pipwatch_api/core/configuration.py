"""This module contains logic responsible for configuring flask-restplus application."""

from configparser import ConfigParser
from logging import config
from os import path
from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


PATH_TO_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config.ini")
PATH_TO_LOG_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "logging.conf")
PATH_TO_LOG_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "./pipwatch-api.log")

CONFIGURATION_FILE: Optional[ConfigParser] = None


def load_config_file() -> ConfigParser:
    """Load configuration file into ConfigParser instance."""
    global CONFIGURATION_FILE  # pylint: disable=global-statement
    if not CONFIGURATION_FILE:
        CONFIGURATION_FILE = ConfigParser()
        CONFIGURATION_FILE.read(PATH_TO_CONFIGURATION_FILE, "utf-8")

    return CONFIGURATION_FILE


def configure_logger() -> None:
    """Apply settings from configuration file to loggers."""
    config.fileConfig(PATH_TO_LOG_CONFIGURATION_FILE)


def configure_sqlalchemy(application: Flask, sql_alchemy_instance: SQLAlchemy) -> None:
    """Initialize SQLAlchemy for flask application."""
    sql_alchemy_instance.init_app(app=application)
    if not application.config.get("PIPWATCHAPI_RESET_DB_ON_START"):
        return

    with application.app_context():
        sql_alchemy_instance.drop_all()
        sql_alchemy_instance.create_all()


def configure_flask_application(application: Flask) -> None:
    """Apply settings from configuration file to flask application instance."""
    # Disable line too long warnings - configuration looks better in one line.
    # pylint: disable=line-too-long
    configuration: ConfigParser = load_config_file()

    application.config["SERVER_NAME"] = configuration.get(section="flask", option="server_name", fallback="127.0.0.1:8080")  # noqa: E501
    application.config["DEBUG"] = configuration.getboolean(section="flask", option="debug", fallback=False)
    application.config["JSON_AS_ASCII"] = configuration.getboolean(section="flask", option="json_as_ascii", fallback=False)  # noqa: E501

    application.config["RESTPLUS_ERROR_404_HELP "] = configuration.getboolean(section="flask-restplus", option="error_404_help", fallback=False)  # noqa: E501
    application.config["RESTPLUS_MASK_SWAGGER "] = configuration.getboolean(section="flask-restplus", option="mask_swagger", fallback=False)  # noqa: E501
    application.config["RESTPLUS_SWAGGER_UI_DOC_EXPANSION"] = configuration.get(section="flask-restplus", option="swagger_ui_doc_expansion", fallback="list")  # noqa: E501
    application.config["RESTPLUS_VALIDATE "] = configuration.getboolean(section="flask-restplus", option="validate", fallback=True)  # noqa: E501

    application.config["SQLALCHEMY_DATABASE_URI"] = configuration.get(section="sql-alchemy", option="database_uri", fallback="sqlite:////db.sqlite")  # noqa: E501
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = configuration.getboolean(section="sql-alchemy", option="track_modifications", fallback=False)  # noqa: E501

    application.config["PIPWATCHAPI_RESET_DB_ON_START"] = configuration.getboolean(section="pipwatch-api", option="resest_db_on_start", fallback=True)  # noqa: E501
