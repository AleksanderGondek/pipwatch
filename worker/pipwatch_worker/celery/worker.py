"""This module contains logic for creating pipwatch worker instance."""

from celery import Celery

from pipwatch_worker.core.configuration import configure_celery_app


worker: Celery = Celery("Pipwatch-worker")
configure_celery_app(celery_app=worker)
