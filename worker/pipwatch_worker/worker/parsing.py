"""This module contains operations related to parsing requirements of project."""
from logging import getLogger, Logger
import os
from typing import Any

import requirements

from pipwatch_worker.core.data_models import Project, RequirementsFile, Requirement
from pipwatch_worker.worker.commands import RepositoriesCacheMixin


class Parse(RepositoriesCacheMixin):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of parsing requirements of given project (and keeping them up to date)."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__()
        self.log = logger or getLogger(__name__)
        self.project_details = project_details

    def __call__(self) -> None:
        """Parse requirements of given project."""
        for requirements_file in self.project_details.requirements_files:
            self.log.debug("Attempting to parse requirements file '{file}'".format(
                file=requirements_file.path
            ))
            self._parse_requirements_file(requirements_file=requirements_file)

    def _parse_requirements_file(self, requirements_file: RequirementsFile) -> None:
        """Parse all packages required by given file."""
        full_path = os.path.join(
            self.repositories_cache_path, self.repositories_cache_dir_name,
            str(self.project_details.id), requirements_file.path
        )

        self.log.debug("Attempting to open file '{file}'".format(file=full_path))
        with open(full_path, "r", encoding="utf-8") as file:
            for requirement_raw in requirements.parse(file):
                self.log.debug("Parsing read requirement of {package}".format(
                    package=repr(requirement_raw)
                ))
                self._parse_requirement(file=requirements_file, requirement=requirement_raw)

    def _parse_requirement(self, file: RequirementsFile, requirement: Any) -> None:
        """Parse single requirement of given file."""
        previous_entry = next((x for x in file.requirements if x.name == requirement.name), None)
        package_version_from_project = str(requirement.specs) if requirement.specs else ""

        if not previous_entry:
            self.log.debug("Previous requirement entry not found. Adding it.")
            file.requirements.append(Requirement(
                name=requirement.name,
                current_version=package_version_from_project
            ))

        if previous_entry and (previous_entry.current_version != package_version_from_project):
            self.log.debug("Overriding {package} version of {prev_version} with {version}".format(
                package=previous_entry.name,
                prev_version=previous_entry.current_version,
                version=package_version_from_project
            ))
            previous_entry.current_version = package_version_from_project
