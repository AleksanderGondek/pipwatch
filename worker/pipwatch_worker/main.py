"""This module contains logic responsible starting the pipwatch worker."""

from logging import getLogger, Logger  # noqa: F401 Imported for type definition
import sys

from celery import Celery  # noqa: F401 Imported for type definition

from pipwatch_worker.core.configuration import configure_logger
from pipwatch_worker.worker import get_celery_worker


def main() -> None:
    """Function to start the whole application."""
    configure_logger()
    log: Logger = getLogger(__name__)

    log.info("Attempting to start worker")
    worker: Celery = get_celery_worker()
    worker.start()
    log.info("Worker started")

    sys.exit(0)


if __name__ == "__main__":
    main()
