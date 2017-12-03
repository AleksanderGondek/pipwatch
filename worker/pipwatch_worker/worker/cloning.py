"""This module contains operations related to cloning project."""
from logging import getLogger, Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git


class Clone:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of cloning given project (and keeping it up to date)."""

    def __init__(self,
                 logger: Logger,
                 project_details: Project) -> None:
        """Create method instance."""
        self.log = logger or getLogger(__name__)
        self.project_details = project_details
        self.git = Git(
            project_id=self.project_details.id,
            project_url=self.project_details.url,
            project_upstream=self.project_details.upstream_url
        )

    def __call__(self) -> None:
        """Clone given repository (or - if it already exists - pull latest changes)."""
        self.log.debug("Attempting to run 'git reset --hard'")
        self.git(command="reset --hard")
        self.log.debug("Attempting to run 'git clean -fd'")
        self.git(command="clean -fd")
        self.log.debug("Attempting to run 'git pull'")
        self.git(command="pull")

        self._handle_upstream_sync()

    def _handle_upstream_sync(self) -> None:
        """Synchronize fork with upstream repository."""
        if not self.project_details.upstream_url:
            return

        self.git(command="fetch upstream")
        self.git(command="merge upstream/master")
