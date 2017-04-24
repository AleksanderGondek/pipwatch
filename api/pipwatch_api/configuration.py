from configparser import ConfigParser
from logging import config
from os import path
from typing import Optional

from flask import Flask


PATH_TO_CONFIGURATION_FILE = path.join(path.dirname(path.abspath(__file__)), "..", "config.ini")
PATH_TO_LOG_CONFIGURATION_FILE = path.join(path.dirname(path.abspath(__file__)), "..", "logging.conf")
PATH_TO_LOG_FILE = path.join(path.dirname(path.abspath(__file__)), "..", "./pipwatch-api.log")


configuration_file: Optional[ConfigParser] = None


def load_config_file() -> ConfigParser:
    """Load configuration file into ConfigParser instance."""
    global configuration_file
    if not configuration_file:
        configuration_file = ConfigParser()
        configuration_file.read(PATH_TO_CONFIGURATION_FILE, "utf-8")

    return configuration_file


def configure_logger() -> None:
    """Apply settings from configuration file to loggers."""
    config.fileConfig(PATH_TO_LOG_CONFIGURATION_FILE)


def configure_flask_application(application: Flask) -> None:
    """Apply settings from configuration file to flask application instance."""
    configuration: ConfigParser = load_config_file()

    application.config["SERVER_NAME"] = configuration.get(section="flask", option="server_name", fallback="127.0.0.1:8080")
    application.config["DEBUG"] = configuration.getboolean(section="flask", option="debug", fallback=False)
    application.config["JSON_AS_ASCII"] = configuration.getboolean(section="flask", option="json_as_ascii", fallback=False)

    application.config["RESTPLUS_ERROR_404_HELP "] = configuration.getboolean(section="flask-restplus", option="error_404_help", fallback=False)
    application.config["RESTPLUS_MASK_SWAGGER "] = configuration.getboolean(section="flask-restplus", option="mask_swagger", fallback=False)
    application.config["RESTPLUS_SWAGGER_UI_DOC_EXPANSION"] = configuration.get(section="flask-restplus", option="swagger_ui_doc_expansion", fallback="list")
    application.config["RESTPLUS_VALIDATE "] = configuration.getboolean(section="flask-restplus", option="validate", fallback=True)
