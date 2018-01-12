"""This module contains operations related to creating github pull request."""
from logging import Logger
from typing import Dict, Union

import requests

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.operations.operation import Operation


class GitReview(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating github pull-review."""

    DEFAULT_PR_TITLE = "[Pipwatch] - Automatic increment of requirements versions."
    DEFAULT_PR_BODY = ""

    def __init__(self, logger: Logger, project_details: Project) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

    def __call__(self) -> None:
        """Create github pull request."""
        raise NotImplementedError()

    def _get_pull_request_body(self) -> Dict[str, Union[bool, str]]:
        """Prepare body for PR creation call."""
        return {
            "title": self.DEFAULT_PR_TITLE,
            "head": "master",
            "base": "master",
            "body": self.DEFAULT_PR_BODY,
            "maintainer_can_modify": True
        }

    def _create_pull_request(self) -> None:
        """Call github http api to create a pull request."""
        url = "{github_api_address}/repos/{owner}/{repo_name}/pulls".format(
            github_api_address=self.project_details.git_repository.github_api_address,
            owner=self.project_details.git_repository.github_project_owner,
            repo_name=self.project_details.git_repository.github_project_owner
        )
        payload = self._get_pull_request_body()
        self.log.debug("About to perform POST request to address '{url}' with payload {payload}".format(
            url=url,
            payload=str(payload)
        ))
        response = requests.post(url=url, json=payload)
        response.raise_for_status()
