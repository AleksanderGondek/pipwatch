"""This module contains broker class for streamlining interaction with celery."""
from typing import Any

from celery import Celery
from celery.result import AsyncResult

from pipwatch_api.core.configuration import configure_celery_app


class Broker:
    """Broker class for interacting with celery application.

    Allows for easy sending celery tasks and retrieving their results.
    """

    def __init__(self) -> None:
        """Initialize class instance."""
        self.app: Celery = Celery("Pipwatch-api")
        configure_celery_app(celery_app=self.app)

    def send_task(self, task_name: str, *args: Any, **kwargs: Any) -> str:
        """Send celery task and receive its id."""
        return self.app.send_task(task_name, args=args, kwargs=kwargs).id

    def check_task(self, task_id: str) -> AsyncResult:
        """Check status of given celery task."""
        return self.app.AsyncResult(task_id)
