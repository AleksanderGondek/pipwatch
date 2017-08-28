"""This module contains celery tasks available for the worker."""

from pipwatch_worker.celery.worker import worker


@worker.task
def task_example(number_one: int, number_two: int) -> int:
    """Example of task, which adds two numbers."""
    return number_one + number_two
