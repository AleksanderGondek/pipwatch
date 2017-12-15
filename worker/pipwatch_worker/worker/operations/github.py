"""This module contains operations related to creating github pull request."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.operations.operation import Operation


class GitReview(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating github pull-review."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

    def __call__(self) -> None:
        """Create github pull request."""
        raise NotImplementedError()
