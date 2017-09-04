"""This module contains states which represent worker current action being undertaken."""

from enum import Enum


class WorkerStates(Enum):
    ATTEMPTING_UPDATE: str = "Attempting_Update"
    CHECKING_FOR_UPDATES: str = "Checking_For_Updates"
    CLEANING_UP: str = "Cleaning_Up"
    CLONING_REPOSITORY: str = "Cloning_Repository"
    COMMITTING_CHANGES: str = "Committing_Changes"
    FAILURE: str = "Failure"
    INITIALIZING: str = "Initializing"
    PARSING_REQUIREMENTS: str = "Parsing_Requirements"
    SUCCESS: str = "Success"
    UPDATING_METADATA: str = "Updating_Metadata"


# pylint: disable=line-too-long
WORKER_STATE_TRANSITIONS = [
    {"trigger": "fail", "source": "*", "dest": WorkerStates.FAILURE.value},
    {"trigger": "clone", "source": WorkerStates.INITIALIZING.value, "dest": WorkerStates.CLONING_REPOSITORY.value},  # noqa: E501
    {"trigger": "parse_requirements", "source": WorkerStates.CLONING_REPOSITORY.value, "dest": WorkerStates.PARSING_REQUIREMENTS.value},  # noqa: E501
    {"trigger": "update_metadata", "source": WorkerStates.PARSING_REQUIREMENTS.value, "dest": WorkerStates.UPDATING_METADATA.value},  # noqa: E501
    {"trigger": "attempt_update", "source": WorkerStates.UPDATING_METADATA.value, "dest": WorkerStates.ATTEMPTING_UPDATE.value},  # noqa: E501
    {"trigger": "commit_changes", "source": WorkerStates.ATTEMPTING_UPDATE.value, "dest": WorkerStates.COMMITTING_CHANGES.value},  # noqa: E501
    {"trigger": "update_metadata", "source": WorkerStates.COMMITTING_CHANGES.value, "dest": WorkerStates.UPDATING_METADATA.value},  # noqa: E501
    {"trigger": "success", "source": WorkerStates.UPDATING_METADATA.value, "dest": WorkerStates.SUCCESS.value}  # noqa: E501
]
