"""This module contains logic responsible starting the pipwatch api."""

from logging import getLogger, Logger  # noqa: F401 Imported for type definition
import sys

from pipwatch_api.core.configuration import configure_logger
from pipwatch_api.application import get_flask_application


def main() -> None:
    """Function to start the whole application"""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start application")
    app = get_flask_application()
    app.run()
    log.info("Application started")

    sys.exit(0)


if __name__ == "__main__":
    main()
