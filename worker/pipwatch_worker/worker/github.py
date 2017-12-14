"""This module contains operations related to creating github pull request."""
from logging import getLogger, Logger

from pipwatch_worker.core.data_models import Project


class GitReview:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating github pull-review."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        self.log = logger or getLogger(__name__)
        self.project_details = project_details

    def __call__(self) -> None:
        """Create github pull request."""
        raise NotImplementedError()
