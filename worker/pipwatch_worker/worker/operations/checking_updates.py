"""This module contains operations related to checking packages updates."""
from logging import Logger
import os
from typing import List, NamedTuple  # noqa: F401 Imported for type definition

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.core.utils import get_pip_script_name
from pipwatch_worker.worker.commands import FromVirtualenv
from pipwatch_worker.worker.operations.operation import Operation


PackageUpdateSuggestion = NamedTuple("PackageUpdateSuggestion", [
    ("name", str),
    ("new_version", str)
])


class CheckUpdates(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of checking for packages updates."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

        self.outdated_packages: List[PackageUpdateSuggestion] = []
        self.from_venv = FromVirtualenv(project_id=self.project_details.id)

    def __call__(self) -> None:
        """Check for packages updates."""
        try:
            self._install_packages()
            self._get_outdated_packages()
            self._update_project_details()
        except Exception:  # pylint: disable=broad-except
            self.log.exception("Unable to check for outdated packages")

    def _install_packages(self) -> None:
        """Install packages of given project to project virtualenv."""
        for requirement_file in self.project_details.requirements_files:
            self.log.debug("Attempting to install requirements from '{file}' to venv.".format(
                file=requirement_file.path
            ))
            self.from_venv(
                command="{pip} install -U -r {file}".format(
                    pip=get_pip_script_name(),
                    file=requirement_file.path
                )
            )

    def _get_outdated_packages(self) -> None:
        """Return list of packages which can be updated."""
        self.log.debug("Attempting to list outdated packages.")
        outcome = self.from_venv(
            command="{pip} list --outdated --format=columns".format(pip=get_pip_script_name())
        )
        if not outcome:
            self.log.debug("No outdated packages found.")
            return

        outcome_as_string = outcome.decode()
        requirements_lines = outcome_as_string.split(os.linesep)
        requirements_detailed = [line.split() for line in requirements_lines[2:] if line]
        self.log.debug("{count} outdated packages found.".format(count=len(requirements_detailed)))
        self.outdated_packages = [
            PackageUpdateSuggestion(requirement[0], requirement[2])
            for requirement in requirements_detailed
        ]

    def _update_project_details(self) -> None:
        """Update desired version of requirement to latest."""
        for changed_package in self.outdated_packages:
            for requirements_file in self.project_details.requirements_files:
                matching_package = next((
                    package for package in requirements_file.requirements
                    if package.name == changed_package.name
                ), None)

                if not matching_package:
                    continue

                if not matching_package.desired_version:
                    matching_package.desired_version = changed_package.new_version
