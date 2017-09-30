"""This module contains logic responsible for starting the pipwatch worker."""

import sys
from logging import getLogger, Logger  # noqa: F401 Imported for type definition

from pipwatch_worker.celery_components.application import app
from pipwatch_worker.core.configuration import configure_logger


def main() -> None:
    """Function to start the whole application."""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start worker")
    app.start()
    log.info("Worker started")

    sys.exit(0)


if __name__ == "__main__":
    main()
