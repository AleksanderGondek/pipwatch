"""This module contains overridden logging.Formatter which saves time in UTC zulu."""

import logging
import time


class UTCFormatter(logging.Formatter):
    """
    Enforce zulu time by default in log entries.

    I could not find any way to achieve this effect from the level of logging configuration file.
    """
    converter = time.gmtime
