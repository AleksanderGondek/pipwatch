"""This module contains pipwatch worker definition."""

from logging import getLogger, Logger  # noqa: F401 Imported for type definition
from typing import Callable

from transitions import Machine

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.checking_updates import CheckUpdates
from pipwatch_worker.worker.attempting_updates import AttemptUpdate
from pipwatch_worker.worker.cloning import Clone
from pipwatch_worker.worker.parsing import Parse
from pipwatch_worker.worker.states import States, WORKER_STATE_TRANSITIONS, Triggers
from pipwatch_worker.worker.updating import Update


class Worker:
    """Responsible for checking and updating python packages in given project."""

    def __init__(self, update_celery_state_method: Callable[[str], None],
                 logger: Logger = None) -> None:
        """Initialize worker instance."""
        self.log: Logger = logger or getLogger(__name__)
        self.state_machine = Machine(
            model=self,
            states=[state.value for state in States],
            initial=States.INITIALIZING.value,
            transitions=WORKER_STATE_TRANSITIONS
        )

        self.project_details: Project = None
        self.update_celery_state = update_celery_state_method

        self.should_attempt_update = False
        self.update_successful = False

        self._attempt_update: Callable[[], None]
        self._clone: Callable[[], None]
        self._parse: Callable[[], None]
        self._update: Callable[[], None]

    def run(self, project_to_process: Project) -> None:
        """Start worker processing of project requirements update request."""
        try:
            self.initialize(project_to_process=project_to_process)
            self.clone()
            self.parse_requirements()
            self.check_updates()
            self.update_metadata()

            if self.should_attempt_update:
                self.attempt_update()
                self.commit_changes()
                self.update_metadata()

            self.success()
        except Exception:
            self.log.exception("Was unable to process update request for project.")
            self.fail()

    def fail(self) -> None:
        """Signify that processing of given request has failed."""
        self.trigger(Triggers.TO_FAIL.value)
        self.update_celery_state(States.FAILURE.value)

    def initialize(self, project_to_process: Project) -> None:
        """Initialize variables needed for further request processing."""
        self.update_celery_state(States.INITIALIZING.value)
        self.project_details = project_to_process

        self._attempt_update = AttemptUpdate(  # type: ignore
            project_details=self.project_details
        )
        self._clone = Clone(  # type: ignore
            project_details=self.project_details
        )
        self._parse = Parse(  # type: ignore
            project_details=self.project_details
        )
        self._check_update = CheckUpdates(  # type: ignore
            self.log, project_details=self.project_details
        )
        self._update = Update(  # type: ignore
            project_details=self.project_details
        )

    def clone(self) -> None:
        """Clone repository containing given project."""
        self.trigger(Triggers.TO_CLONE.value)
        self.update_celery_state(States.CLONING_REPOSITORY.value)
        self._clone()

    def parse_requirements(self) -> None:
        """Parse and load requirements that are needed by given project."""
        self.trigger(Triggers.TO_PARSE_REQ.value)
        self.update_celery_state(States.PARSING_REQUIREMENTS.value)
        self._parse()

    def check_updates(self) -> None:
        """Check if any of given required packages may be updated."""
        self.trigger(Triggers.TO_CHECK_UPDATES.value)
        self.update_celery_state(States.CHECKING_FOR_UPDATES.value)
        self.should_attempt_update = self._check_update()

    def update_metadata(self) -> None:
        """Send update of given project information (with possible new requirements versions)."""
        self.trigger(Triggers.TO_UPDATE_META.value)
        self.update_celery_state(States.UPDATING_METADATA.value)
        self._update()

    def attempt_update(self) -> None:
        """Check if update of given packages will break project."""
        self.trigger(Triggers.TO_UPDATE_PGS.value)
        self.update_celery_state(States.ATTEMPTING_UPDATE.value)

        try:
            self._attempt_update()
        except:
            self.update_successful = False
        else:
            self.update_successful = True

    def commit_changes(self) -> None:
        """Commit changes to given project."""
        self.trigger(Triggers.TO_COMMIT.value)
        self.update_celery_state(States.COMMITTING_CHANGES.value)
        if not self.update_successful:
            return

    def success(self) -> None:
        """Signify that processing of given request has succeeded."""
        self.trigger(Triggers.TO_SUCCESS.value)
        self.update_celery_state(States.SUCCESS.value)

    def trigger(self, transition_trigger: str) -> None:
        """This will be overridden by transitions.Machine"""
