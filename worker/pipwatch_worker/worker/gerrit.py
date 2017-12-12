"""This module contains operations related to creating gerrit patchset."""
from logging import getLogger, Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import FromVirtualenv, RepositoriesCacheMixin


class GitReview(RepositoriesCacheMixin):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating git-review and submitting it."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__()
        self.log = logger or getLogger(__name__)
        self.project_details = project_details
        self.from_venv = FromVirtualenv(project_id=self.project_details.id)

    def __call__(self) -> None:
        """Create gerrit patchset and submit it."""
        self.from_venv(
            command="git-review"
        )
