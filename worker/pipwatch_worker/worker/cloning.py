"""This module contains operations related to cloning project."""
import os
import subprocess


class Cloner:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of cloning and keeping up to date given git repository."""
    REPOSITORY_DIRECTORY: str = "projects"

    def __init__(self, clone_into_dir_name: str, project_url: str) -> None:
        """Initialize class instance."""
        self.directory_name = clone_into_dir_name
        self.project_url = project_url

    def clone_and_pull_latest(self) -> None:
        """Clone given git repository (if it already exists, it will be cleaned and pulled)."""
        os.makedirs(self.repository_path, exist_ok=True)
        if os.path.exists(self.path_to_cloned_project):
            self._clean_and_pull()
            return

        self._clone()

    @property
    def repository_path(self) -> str:
        """Return full path to directory containing projects."""
        return os.path.join(os.getcwd(), self.REPOSITORY_DIRECTORY)

    @property
    def path_to_cloned_project(self) -> str:
        """Return full path to directory containing project."""
        return os.path.join(self.repository_path, self.directory_name)

    def _clean_and_pull(self) -> None:
        """Reset any changes made to repository and pull latest changes."""
        subprocess.run(args="git rest --hard && git clean -fd && git pull",
                       cwd=self.path_to_cloned_project,
                       shell=False,
                       check=True)

    def _clone(self) -> None:
        """Clone git project."""
        subprocess.run(args="git clone {} {}".format(self.project_url, self.directory_name),
                       cwd=self.repository_path,
                       shell=False,
                       check=True)
