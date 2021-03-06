"""This module contains operations related to updating requirements status of project in db."""
from configparser import ConfigParser  # noqa: F401 Imported for type definition
from logging import Logger

import requests

from pipwatch_worker.core.configuration import load_config_file
from pipwatch_worker.core.data_models import Project, RequirementsFile
from pipwatch_worker.worker.operations.operation import Operation


class Update(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of sending update of project requirements."""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        self.config: ConfigParser = load_config_file()

    def __call__(self) -> None:
        """Send updates for each requirement file."""
        for requirements_file in self.project_details.requirements_files:
            self.log.debug("Attempting to send updated state of requirements file '{file}'".format(
                file=requirements_file.path
            ))
            self._update_requirements_file(file=requirements_file)

    def _update_requirements_file(self, file: RequirementsFile) -> None:
        """Send update of provided requirements file."""
        url = "{api_address}/api/v1/requirements-files/{file_id}".format(
            api_address=self.config.get(section="pipwatch-api", option="address", fallback="pipwatch_api:80880"),
            file_id=str(file.id)
        )
        payload = file.to_dict()
        self.log.debug("About to perform PUT request to address '{url}' with payload {payload}".format(
            url=url,
            payload=payload
        ))
        response = requests.put(url=url, json=payload)
        response.raise_for_status()
