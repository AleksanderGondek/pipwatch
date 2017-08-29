"""This module contains logic responsible for configuring the worker."""

from configparser import ConfigParser
from logging import config
from os import path
from typing import Optional

from celery import Celery  # noqa: F401 Imported for type definition


PATH_TO_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config.ini")
PATH_TO_LOG_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "logging.conf")

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


def configure_celery_app(celery_app: Celery) -> None:
    """Apply configuration settings to celery application instance."""
    config: ConfigParser = load_config_file()
    celery_app.conf.update(
        broker_url=config.get(section="celery", option="broker_url", fallback="redis://localhost:6379/0"),
        enable_utc=config.getboolean(section="celery", option="enable_utc", fallback=False),
        imports=config.get(section="celery", option="imports", fallback="pipwatch_worker.celery.tasks").split(","),
        result_backend =config.get(section="celery", option="result_backend", fallback="redis://localhost:6379/0")
    )
