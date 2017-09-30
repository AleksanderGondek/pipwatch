"""This module contains celery tasks available for the worker."""
from typing import Any, Dict

from pipwatch_worker.celery_components.application import app
from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.worker import Worker


@app.task(bind=True, retry_backoff=True)
def process_project(self, processing_request: Dict[str, Any]) -> None:
    """Check if packages in given project may be updated."""
    worker = Worker(update_celery_state_method=self.update_state)
    project_processing_request: Project = Project.from_dict(dictionary=processing_request)
    worker.run(project_to_process=project_processing_request)
