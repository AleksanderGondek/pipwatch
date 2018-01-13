"""This module contains operations related to pushing git changes."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class GitPush(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of pushing git changes up to parent repository."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        self.git = Git(self.project_details.id, self.project_details.git_repository.url)

    def __call__(self) -> None:
        """Push git changes."""
        self.log.debug("Attempting to run 'git push' command..")
        self.git("push")
