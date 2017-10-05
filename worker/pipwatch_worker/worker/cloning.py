"""This module contains operations related to cloning project."""
from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git


class Clone:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of cloning given project (and keeping it up to date)."""

    def __init__(self, project_details: Project) -> None:
        """Create method instance."""
        self.project_details = project_details
        self.git = Git(project_id=self.project_details.id, project_url=self.project_details.url)

    def __call__(self) -> None:
        """Clone given repository (or - if it already exists - pull latest changes)."""
        self.git(command="reset --hard")
        self.git(command="clean -fd")
        self.git(command="pull")
