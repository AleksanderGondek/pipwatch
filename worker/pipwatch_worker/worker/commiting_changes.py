"""This module contains operations related to committing and reviewing changes done to requirements."""
from logging import Logger, getLogger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git


class CommitChanges:  # pylint: disable=too-few-public-methods
    """Encompasses logic of committing changes made to requirements.

    Note: In future this class should NOT push changes but instead do a pull-request/gerrit-patch.
    """

    DEFAULT_COMMIT_MSG = "[Pipwatch] - Automatic increment of requirements versions."

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Initialize method instance."""
        self.project_details = project_details
        self.log: Logger = logger or getLogger(__name__)
        self.git = Git(self.project_details.id, self.project_details.url)

    def __call__(self, commit_msg: str = None) -> None:
        """Commit changes and push them to master branch."""
        for requirements_file in self.project_details.requirements_files:
            self.git("add {file}".format(file=requirements_file.path))

        commit_msg = commit_msg if commit_msg else self.DEFAULT_COMMIT_MSG
        self.git("commit -m {}".format(commit_msg))
        self.git("push origin/master")