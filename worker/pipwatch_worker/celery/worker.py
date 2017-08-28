"""This module contains logic for creating pipwatch worker instance."""

from celery import Celery


worker: Celery = Celery("Pipwatch-worker")
worker.config_from_object("pipwatch_worker.celery.celeryconfig")
