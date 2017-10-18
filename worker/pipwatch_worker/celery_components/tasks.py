"""This module contains celery tasks available for the worker."""
from logging import getLogger, Logger  # noqa: F401 Imported for type definition
from typing import Any, Dict

from pipwatch_worker.celery_components.application import app
from pipwatch_worker.core.configuration import configure_logger
from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.worker import Worker


configure_logger()
log: Logger = getLogger(__name__)


@app.task(bind=True)
def process_project(self, processing_request: Dict[str, Any]) -> None:
    """Check if packages in given project may be updated."""
    log.debug("Starting task 'process_project'.")
    worker = Worker(update_celery_state_method=self.update_state, logger=log)

    log.debug("Attempting to deserialize project request.")
    project_processing_request: Project = Project.from_dict(dictionary=processing_request)

    log.debug("Run starting.")
    worker.run(project_to_process=project_processing_request)
