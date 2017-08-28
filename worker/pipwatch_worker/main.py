"""This module contains logic responsible starting the pipwatch worker."""

import sys
from logging import getLogger, Logger  # noqa: F401 Imported for type definition

from celery import Celery  # noqa: F401 Imported for type definition

from pipwatch_worker.celery.worker import worker
from pipwatch_worker.core.configuration import configure_logger


def main() -> None:
    """Function to start the whole application."""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start worker")
    worker.start()
    log.info("Worker started")

    sys.exit(0)


if __name__ == "__main__":
    main()
