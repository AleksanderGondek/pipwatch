"""This module contains operations related to updating requirements of project."""
import os

from pipwatch_worker.core.data_models import Project, RequirementsFile
from pipwatch_worker.worker.commands import Command, FromVirtualenv, Git, RepositoriesCacheMixin


class AttemptUpdate(RepositoriesCacheMixin):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of attempt of updating requirements of given project."""

    def __init__(
            self,
            project_details: Project
    ) -> None:
        """Create method instance."""
        super().__init__()
        self.project_details = project_details
        self.command = Command(project_id=self.project_details.id)
        self.from_venv = FromVirtualenv(project_id=self.project_details.id)
        self.git = Git(
            project_id=self.project_details.id,
            project_url=self.project_details.url
        )

    def __call__(self) -> None:
        """Update requirements of given project."""
        for requirements_file in self.project_details.requirements_files:
            self._update_requirement_file(requirements_file=requirements_file)
            self.from_venv(
                command="{pip} install -U -r {file}".format(
                    pip=self._pip_script_name,
                    file=requirements_file.path
                )
            )
        self._check()

    def _check(self) -> bool:
        """Validate if new packages did not break the project."""
        self.command(command=self.project_details.check_command)
        return True

    def _update_requirement_file(self, requirements_file: RequirementsFile) -> None:
        """Save new requirements."""
        full_path = os.path.join(
            self.repositories_cache_path, self.repositories_cache_dir_name,
            str(self.project_details.id), requirements_file.path
        )

        os.remove(full_path)
        with open(full_path, "w", encoding="utf-8") as file:
            for requirement in sorted(requirements_file.requirements, key=lambda x: x.name):
                file.write("{name}{version}".format(
                    name=requirement.name,
                    version=requirement.desired_version
                ))

    @property
    def _pip_script_name(self) -> str:
        """Return expected pip script name for os pipwatch is currently running on."""
        script_name = "pip"
        if os.name == "nt":
            script_name += ".exe"

        return script_name
