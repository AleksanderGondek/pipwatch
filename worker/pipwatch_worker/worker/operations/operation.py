"""This module contains worker operation interface definition."""
from logging import getLogger, Logger

from pipwatch_worker.worker.commands import RepositoriesCacheMixin
from pipwatch_worker.core.data_models import Project


class Operation(RepositoriesCacheMixin):  # pylint: disable=too-few-public-methods
    """Defines common interface for different operations that worker may perform on a project."""

    def __init__(
            self,
            logger: Logger,
            project_details: Project
    ) -> None:
        """Create method instance."""
        super().__init__()
        self.log = logger or getLogger(__name__)
        self.project_details = project_details

    def __call__(self) -> None:
        """Run operation (need to be overridden and implemented)."""
        raise NotImplementedError()
