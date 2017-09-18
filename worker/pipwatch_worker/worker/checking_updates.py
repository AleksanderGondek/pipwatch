"""This module contains operations related to checking packages updates."""
from logging import Logger, getLogger
import os
from typing import List, NamedTuple  # noqa: F401 Imported for type definition

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import FromVirtualenv


PackageUpdateSuggestion = NamedTuple("PackageUpdateSuggestion", [
    ("name", str),
    ("new_version", str)
])


class CheckUpdates:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of checking for packages updates."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        self.project_details = project_details
        self.log: Logger = logger or getLogger(__name__)

        self._outdated_packages: List[PackageUpdateSuggestion] = None
        self.from_venv = FromVirtualenv(project_id=self.project_details.id)

    def __call__(self) -> bool:
        """Check for packages updates."""
        try:
            self._install_packages()
            self._get_outdated_packages()
            self._update_project_details()
        except Exception:  # pylint: disable=broad-except
            self.log.exception("Unable to check for outdated packages")

        return bool(self._outdated_packages)

    def _install_packages(self) -> None:
        """Install packages of given project to project virtualenv."""
        for requirement_file in self.project_details.requirements_files:
            self.from_venv(command="pip install -U -r {}".format(requirement_file.path))

    def _get_outdated_packages(self) -> None:
        """Return list of packages which can be updated."""
        outcome = self.from_venv(command="pip list --outdated --format=columns")
        if not outcome:
            return

        outcome_as_string = outcome.decode()
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
