"""This module contains worker logic."""

from enum import Enum


class WorkerStates(Enum):
    ATTEMPTING_UPDATE: str = "Attempting_Update"
    CHECKING_FOR_UPDATES: str = "Checking_For_Updates"
    CLEANING_UP: str = "Cleaning_Up"
    CLONING_REPOSITORY: str = "Cloning_Repository"
    COMMITTING_CHANGES: str = "Committing_Changes"
    FAILURE: str = "Failure"
    INITIALIZING: str =  "Initializing"
    PARSING_REQUIREMENTS: str = "Parsing_Requirements"
    SUCCESS: str = "Success"
    UPDATING_METADATA: str = "Updating_Metadata"


WORKER_STATE_TRANSITIONS = [
    {"trigger": "fail", "source": "*", "dest": WorkerStates.FAILURE.value},
    {"trigger": "clone", "source": WorkerStates.INITIALIZING.value, "dest": WorkerStates.CLONING_REPOSITORY.value},
    {"trigger": "parse_requirements", "source": WorkerStates.CLONING_REPOSITORY.value, "dest": WorkerStates.PARSING_REQUIREMENTS.value},
    {"trigger": "update_metadata", "source": WorkerStates.PARSING_REQUIREMENTS.value, "dest": WorkerStates.UPDATING_METADATA.value},
    {"trigger": "attempt_update", "source": WorkerStates.UPDATING_METADATA.value, "dest": WorkerStates.ATTEMPTING_UPDATE.value},
    {"trigger": "commit_changes", "source": WorkerStates.ATTEMPTING_UPDATE.value, "dest": WorkerStates.COMMITTING_CHANGES.value},
    {"trigger": "update_metadata", "source": WorkerStates.COMMITTING_CHANGES.value, "dest": WorkerStates.UPDATING_METADATA.value},
    {"trigger": "success", "source": WorkerStates.UPDATING_METADATA.value, "dest": WorkerStates.SUCCESS.value}
]
