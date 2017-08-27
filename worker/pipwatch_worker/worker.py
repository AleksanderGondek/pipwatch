"""This module contains logic for creating pipwatch worker instance."""

from typing import Optional

from celery import Celery

from pipwatch_worker.core.configuration import PATH_CELERY_CONFIG_FILE

WORKER: Optional[Celery] = None


def get_celery_worker() -> Celery:
    """Return configured Celery application."""
    global WORKER  # pylint: disable=global-statement
    if not WORKER:
        WORKER = Celery("Pipwatch-worker")
        WORKER.config_from_object(PATH_CELERY_CONFIG_FILE)

    return WORKER
