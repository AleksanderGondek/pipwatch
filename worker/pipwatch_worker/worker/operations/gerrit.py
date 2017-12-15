"""This module contains operations related to creating gerrit patchset."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import FromVirtualenv
from pipwatch_worker.worker.operations.operation import Operation


class GitReview(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating git-review and submitting it."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        self.from_venv = FromVirtualenv(project_id=self.project_details.id)

    def __call__(self) -> None:
        """Create gerrit patchset and submit it."""
        self.log.debug("Attempting to run 'git-review' command..")
        self.from_venv(
            command="git-review"
        )
