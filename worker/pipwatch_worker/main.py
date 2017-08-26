"""This module contains logic responsible starting the pipwatch worker."""

from logging import getLogger, Logger  # noqa: F401 Imported for type definition
import sys

from pipwatch_worker.core.configuration import configure_logger


def main() -> None:
    """Function to start the whole application."""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start application")
    log.info("Application started")

    sys.exit(0)


if __name__ == "__main__":
    main()
