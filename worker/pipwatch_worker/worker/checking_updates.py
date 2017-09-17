"""This module contains operations related to checking packages updates."""
from logging import Logger, getLogger
import os
import shutil
import subprocess
from typing import List, NamedTuple

from pipwatch_worker.core.data_models import Project


PackageUpdateSuggestion = NamedTuple("PackageUpdateSuggestion", [
    ("name", str),
    ("new_version", str)
])


class CheckUpdates:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of checking for packages updates."""

    VIRTUALENV_COMMAND = "virtualenv"
    VIRTUALENV_DIRECTORY = ".virtualenv"

    def __init__(self, logger: Logger, repository_directory: str, project_details: Project) -> None:
        """Create method instance."""
        self.repository_directory_name = repository_directory
        self.project_details = project_details
        self.log: Logger = logger or getLogger(__name__)

        self._outdated_packages: List[PackageUpdateSuggestion] = None

    def __call__(self) -> List[PackageUpdateSuggestion]:
        """Check for packages updates."""
        outdated: List[PackageUpdateSuggestion] = []
        try:
            self._create_virtualenv()
            self._install_packages()
            self._get_outdated_packages()
            self._update_project_details()
        except Exception:  # pylint: disable=broad-except
            self.log.exception("Unable to check for outdated packages")
        finally:
            self._remove_virtualenv()

        return outdated

    @property
    def cloned_project_path(self) -> str:
        """Return full path to directory that should contain cloned project."""
        return os.path.join(os.getcwd(), self.repository_directory_name, str(self.project_details.id))

    @property
    def pip_command_path(self) -> str:
        """Return relative path to pip executable from project virtualenv."""
        pip_holder = "bin" if os.name != "nt" else "Scripts"
        return os.path.join(self.VIRTUALENV_DIRECTORY, pip_holder, "pip")

    def _create_virtualenv(self) -> None:
        """Create virtualenv for given project."""
        subprocess.run(
            args="{virtualenv} {dir} --python=python3".format(
                virtualenv=self.VIRTUALENV_COMMAND,
                dir=self.VIRTUALENV_DIRECTORY
            ),
            cwd=self.cloned_project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=True
        )

    def _install_packages(self) -> None:
        """Install packages of given project to project virtualenv."""
        args = "{pip} install -U".format(pip=self.pip_command_path)
        for requirement_file in self.project_details.requirements_files:
            args += " -r {}".format(requirement_file.path)

        subprocess.run(
            args=args,
            cwd=self.cloned_project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=True
        )

    def _remove_virtualenv(self) -> None:
        """Remove virtualenv for given project."""
        shutil.rmtree(path=os.path.join(self.cloned_project_path, self.VIRTUALENV_DIRECTORY))

    def _get_outdated_packages(self) -> None:
        """Return list of packages which can be updated."""
        outcome = subprocess.run(
            args="{pip} list --outdated --format=columns".format(
                pip=self.pip_command_path
            ),
            cwd=self.cloned_project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=True
        )

        if not outcome.stdout:
            return

        outcome_as_string = outcome.stdout.decode()
        requirements_lines = outcome_as_string.split(os.linesep)
        requirements_detailed = [line.split() for line in requirements_lines if line]
        self._outdated_packages = [
            PackageUpdateSuggestion(requirement[0], requirement[2])
            for requirement in requirements_detailed
        ]

    def _update_project_details(self) -> None:
        """Update desired version of requirement to latest."""
        for changed_package in self._outdated_packages:
            for requirements_file in self.project_details.requirements_files:
                matching_package = next((
                    package for package in requirements_file.requirements
                    if package.name == changed_package.name
                ), None)

                matching_package.desired_version = changed_package.new_version
