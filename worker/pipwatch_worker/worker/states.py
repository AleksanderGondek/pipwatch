"""This module contains states which represent worker current action being undertaken."""

from enum import Enum


class States(Enum):
    ATTEMPTING_UPDATE: str = "Attempting_Update"
    CHECKING_FOR_UPDATES: str = "Checking_For_Updates"
    CLONING_REPOSITORY: str = "Cloning_Repository"
    COMMITTING_CHANGES: str = "Committing_Changes"
    FAILURE: str = "Failure"
    INITIALIZING: str = "Initializing"
    PARSING_REQUIREMENTS: str = "Parsing_Requirements"
    SUCCESS: str = "Success"
    UPDATING_METADATA: str = "Updating_Metadata"


class Triggers(Enum):
    TO_CHECK_UPDATES: str = "to_check_updates"
    TO_CLONE: str = "to_clone"
    TO_COMMIT: str = "to_commit_changes"
    TO_FAIL: str = "to_fail"
    TO_PARSE_REQ: str = "to_parse_requirements"
    TO_SUCCESS: str = "to_success"
    TO_UPDATE_META: str = "to_update_metadata"
    TO_UPDATE_PGS: str = "to_attempt_update"


WORKER_STATE_TRANSITIONS = [
    {
        "source": "*",
        "dest": States.FAILURE.value,
        "trigger": Triggers.TO_FAIL.value
    },
    {
        "source": States.INITIALIZING.value,
        "dest": States.CLONING_REPOSITORY.value,
        "trigger": Triggers.TO_CLONE.value
    },
    {
        "source": States.CLONING_REPOSITORY.value,
        "dest": States.PARSING_REQUIREMENTS.value,
        "trigger": Triggers.TO_PARSE_REQ.value
    },
    {
        "source": States.PARSING_REQUIREMENTS.value,
        "dest": States.CHECKING_FOR_UPDATES.value,
        "trigger": Triggers.TO_CHECK_UPDATES.value
    },
    {
        "source": States.CHECKING_FOR_UPDATES.value,
        "dest": States.UPDATING_METADATA.value,
        "trigger": Triggers.TO_UPDATE_META.value
    },
    {
        "source": States.UPDATING_METADATA.value,
        "dest": States.ATTEMPTING_UPDATE.value,
        "trigger": Triggers.TO_UPDATE_PGS.value
    },
    {
        "source": States.ATTEMPTING_UPDATE.value,
        "dest": States.COMMITTING_CHANGES.value,
        "trigger": Triggers.TO_COMMIT.value
    },
    {
        "source": States.COMMITTING_CHANGES.value,
        "dest": States.UPDATING_METADATA.value,
        "trigger": Triggers.TO_UPDATE_META.value
    },
    {
        "source": States.UPDATING_METADATA.value,
        "dest": States.SUCCESS.value,
        "trigger": Triggers.TO_SUCCESS.value
    }
]
