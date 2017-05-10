"""This module contains logic responsible starting the pipwatch api."""

from logging import getLogger, Logger
import sys

from pipwatch_api.core.configuration import configure_logger
from pipwatch_api.application import get_flask_application


def main() -> int:
    """Function to start the whole application"""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start application")
    app = get_flask_application()
    app.run()
    log.info("Application started")

    return sys.exit(0)


if __name__ == "__main__":
    main()
