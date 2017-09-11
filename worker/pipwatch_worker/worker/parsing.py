"""This module contains operations related to parsing requirements of project."""
import os
from typing import Any

import requirements

from pipwatch_worker.core.data_models import Project, RequirementsFile, Requirement


class Parse:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of parsing requirements of given project (and keeping them up to date)."""

    def __init__(self, repository_directory: str, project_details: Project) -> None:
        """Create method instance."""
        self.repository_directory_name = repository_directory
        self.project_details = project_details

    def __call__(self) -> None:
        """Parse requirements of given project."""
        for requirements_file in self.project_details.requirements_files:
            self._parse_requirements_file(requirements_file=requirements_file)

    def _parse_requirements_file(self, requirements_file: RequirementsFile) -> None:
        """Parse all packages required by given file."""
        full_path = os.path.join(os.getcwd(), self.repository_directory_name, str(requirements_file.id))
        with open(full_path, "r", encoding="utf-8") as file:
            for requirement_raw in requirements.parse(file):
                self._parse_requirement(file=requirements_file, requirement=requirement_raw)

    @staticmethod
    def _parse_requirement(file: RequirementsFile, requirement: Any) -> None:
        """Parse single requirement of given file."""
        previous_entry = next((x for x in file.requirements if x.name == requirement.name), None)
        if not previous_entry:
            file.requirements.append(Requirement(
                name=requirement.name,
                current_version=str(requirement.specs),
                desired_version=str(requirement.specs)
            ))

        package_version_from_project = str(requirement.specs)
        if previous_entry.current_version != package_version_from_project:
            previous_entry.desired_version = package_version_from_project
