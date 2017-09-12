"""This module contains operations related to updating requirements status of project in db."""
from configparser import ConfigParser

import requests

from pipwatch_worker.core.configuration import load_config_file
from pipwatch_worker.core.data_models import Project, RequirementsFile


class Update():  # pylint: disable=too-few-public-methods
    """Encapsulates logic of sending update of project requirements."""

    def __init__(self, project_details: Project) -> None:
        """Create method instance."""
        self.config: ConfigParser = load_config_file()
        self.project_details: Project = project_details

    def __call__(self) -> None:
        """Send updates for each requirement file."""
        for requirements_file in self.project_details.requirements_files:
            self._update_requirements_file(file=requirements_file)

    def _update_requirements_file(self, file: RequirementsFile) -> None:
        """Send update of provided requirements file."""
        url = "{api_address}/api/v1/requirements-files/{file_id}".format(
            api_address=self.config.get(section="pipwatch-api", option="address", fallback="pipwatch_api:80880"),
            file_id=str(file.id)
        )
        response = requests.put(url=url, data=file.to_dict())
        response.raise_for_status()
