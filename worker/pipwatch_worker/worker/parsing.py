"""This module contains operations related to parsing requirements of project."""
import os
from typing import List, Dict, Set

import requirements

from pipwatch_worker.core.data_models import Requirement


class Parser:  # pylint: disable=too-few-public-methods
    """Encapsulates logic of retrieving difference between requirements in project and pipwatch db."""

    def __init__(self,
                 directory_name: str,
                 requirements_files_paths: List[str],
                 requirements_from_db: Dict[str, Requirement]) -> None:
        """Initialize class instance."""
        self.directory_name: str = directory_name
        self.requirements_files_paths: List[str] = requirements_files_paths
        self.requirements_from_db: Dict[str, Requirement] = requirements_from_db

    def get_requirements_diff(self) -> Set[Requirement]:
        """Retrieve list of requirements that need to be updated in db."""
        difference = set()
        for requirement in self._get_requirements_from_project_files():
            if requirement.name not in self.requirements_from_db:
                difference.add(requirement)
                continue

            requirement_from_db = self.requirements_from_db[requirement.name]
            if requirement.current_version != requirement_from_db.current_version:
                difference.add(requirement)
                continue

        return difference

    def _get_requirements_from_project_files(self) -> Set[Requirement]:
        """Retrieve list of all requirements specified in all requirements files."""
        all_requirements: Set = set()
        for requirements_file in self.requirements_files_paths:
            full_path = os.path.join(os.getcwd(), self.directory_name, requirements_file)
            all_requirements = all_requirements.union(self._get_requirements_for_file(full_path))

        return all_requirements

    @staticmethod
    def _get_requirements_for_file(full_path) -> Set[Requirement]:
        """Retrieve list of requirements from single file provided."""
        with open(full_path, "r", encoding="utf-8") as file:
            return set(
                Requirement(name=requirement.name, current_version=str(requirement.specs))
                for requirement in requirements.parse(file)
            )
