"""This module contains operations related to cloning project."""
import os
import subprocess

from pipwatch_worker.core.data_models import Project


class Clone:
    """Encapsulates logic of cloning given project (and keeping it up to date)."""

    def __init__(self, repository_directory: str, project_details: Project) -> None:
        """Create method instance."""
        self.repository_directory_name = repository_directory
        self.project_details = project_details

    def __call__(self) -> None:
        """Clone given repository (or - if it already exists - pull latest changes)."""
        os.makedirs(self.repository_path, exist_ok=True)
        if os.path.exists(self.cloned_project_path):
            self._clean_and_pull()
            return

        self._clone()

    @property
    def repository_path(self) -> str:
        """Return full path to directory that should be root of all cloned projects."""
        return os.path.join(os.getcwd(), self.repository_directory_name)

    @property
    def cloned_project_path(self) -> str:
        """Return full path to directory that should contain cloned project."""
        return os.path.join(self.repository_path,  self.project_details.id)

    def _clean_and_pull(self) -> None:
        """Perform hard reset of repository and pull latest changes."""
        subprocess.run(args="git rest --hard && git clean -fd && git pull",
                       cwd=self.cloned_project_path,
                       shell=False,
                       check=True)

    def _clone(self) -> None:
        """Clone given project."""
        subprocess.run(args="git clone {} {}".format(self.project_details.url, self.project_details.id),
                       cwd=self.repository_path,
                       shell=False,
                       check=True)
