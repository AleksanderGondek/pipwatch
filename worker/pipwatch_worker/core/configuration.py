"""This module contains logic responsible for configuring the worker."""

from configparser import ConfigParser
from logging import config
from os import path
from typing import Optional


PATH_TO_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "config.ini")
PATH_TO_LOG_CONFIGURATION_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "logging.conf")
PATH_TO_LOG_FILE: str = path.join(path.dirname(path.abspath(__file__)), "../..", "./pipwatch-worker.log")
PATH_CELERY_CONFIG_FILE: str = path.join(path.dirname(path.abspath(__file__)), "..", "celeryconfig.py")

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
