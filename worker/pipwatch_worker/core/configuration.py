"""This module contains logic responsible for configuring the worker."""

from configparser import ConfigParser
from logging import config
from os import path
from typing import Optional

from celery import Celery  # noqa: F401 Imported for type definition

# Disable line too long warnings - configuration looks better in one line.
# pylint: disable=line-too-long

PATH_TO_DEFAULT_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config.ini")  # noqa: E501
PATH_TO_OVERRIDE_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config-override.ini")  # noqa: E501
PATH_TO_LOG_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "logging.conf")  # noqa: E501

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
