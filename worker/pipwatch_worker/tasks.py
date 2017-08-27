"""This module contains celery tasks available for the worker."""

from celery import Celery

from pipwatch_worker.worker import get_celery_worker


worker: Celery = get_celery_worker()


@worker.task
def task_example(number_one: int, number_two: int) -> int:
    """Example of task, which adds two numbers."""
    return number_one + number_two
