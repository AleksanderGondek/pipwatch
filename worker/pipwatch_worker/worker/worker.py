"""This module contains pipwatch worker definition."""

from configparser import ConfigParser
from itertools import chain
from logging import getLogger, Logger  # noqa: F401 Imported for type definition
from typing import Callable, FrozenSet  # noqa: F401 Imported for type definition

from transitions import Machine

from pipwatch_worker.core.configuration import load_config_file
from pipwatch_worker.core.data_models import Project
from pipwatch_worker.core.utils import ProjectFlavour
from pipwatch_worker.worker.operations.checking_updates import CheckUpdates
from pipwatch_worker.worker.operations.attempting_updates import AttemptUpdate
from pipwatch_worker.worker.operations.cloning import Clone
from pipwatch_worker.worker.operations.commiting_changes import CommitChanges
from pipwatch_worker.worker.operations.gerrit import GitReview
from pipwatch_worker.worker.operations.github import PullRequest
from pipwatch_worker.worker.operations.git_push import GitPush
from pipwatch_worker.worker.operations.operation import Operation
from pipwatch_worker.worker.operations.parsing import Parse
from pipwatch_worker.worker.states import States, WORKER_STATE_TRANSITIONS, Triggers
from pipwatch_worker.worker.operations.updating import Update


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

        self._locked_packages_ids: FrozenSet[int] = frozenset()

        self._attempt_update: Operation
        self._commit_changes: Operation
        self._clone: Operation
        self._git_review: Operation
        self._git_push: Operation
        self._parse: Operation
        self._pull_request: Operation
        self._update: Operation

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
                self.push_changes()
                self.update_metadata()

            self.success()
        except Exception:
            self.log.exception("Was unable to process update request for project.")
            self.fail()

    def fail(self) -> None:
        """Signify that processing of given request has failed."""
        self.log.debug("Changing state to {state}.".format(state=States.FAILURE.value))
        self.trigger(Triggers.TO_FAIL.value)
        self.update_celery_state(States.FAILURE.value)

    def initialize(self, project_to_process: Project) -> None:
        """Initialize variables needed for further request processing."""
        self.log.debug("Changing state to {state}.".format(state=States.INITIALIZING.value))
        self.update_celery_state(States.INITIALIZING.value)
        self.project_details = project_to_process

        self._save_packages_with_locked_versions()

        self._attempt_update = AttemptUpdate(
            logger=self.log, project_details=self.project_details
        )
        self._check_update = CheckUpdates(
            logger=self.log, project_details=self.project_details
        )
        self._clone = Clone(
            logger=self.log, project_details=self.project_details
        )
        self._commit_changes = CommitChanges(
            logger=self.log, project_details=self.project_details
        )
        self._git_push = GitPush(
            logger=self.log, project_details=self.project_details
        )
        self._git_review = GitReview(
            logger=self.log, project_details=self.project_details
        )
        self._parse = Parse(
            logger=self.log, project_details=self.project_details
        )
        self._pull_request = PullRequest(
            logger=self.log, project_details=self.project_details
        )
        self._update = Update(
            logger=self.log, project_details=self.project_details
        )

    def clone(self) -> None:
        """Clone repository containing given project."""
        self.log.debug("Changing state to {state}.".format(state=States.CLONING_REPOSITORY.value))
        self.trigger(Triggers.TO_CLONE.value)
        self.update_celery_state(States.CLONING_REPOSITORY.value)
        self._clone()

    def parse_requirements(self) -> None:
        """Parse and load requirements that are needed by given project."""
        self.log.debug("Changing state to {state}.".format(state=States.PARSING_REQUIREMENTS.value))
        self.trigger(Triggers.TO_PARSE_REQ.value)
        self.update_celery_state(States.PARSING_REQUIREMENTS.value)
        self._parse()

    def check_updates(self) -> None:
        """Check if any of given required packages may be updated."""
        self.log.debug("Changing state to {state}.".format(state=States.CHECKING_FOR_UPDATES.value))
        self.trigger(Triggers.TO_CHECK_UPDATES.value)
        self.update_celery_state(States.CHECKING_FOR_UPDATES.value)
        self._check_update()
        self.should_attempt_update = bool(self._check_update.outdated_packages)

    def update_metadata(self) -> None:
        """Send update of given project information (with possible new requirements versions)."""
        self.log.debug("Changing state to {state}.".format(state=States.UPDATING_METADATA.value))
        self.trigger(Triggers.TO_UPDATE_META.value)
        self.update_celery_state(States.UPDATING_METADATA.value)

        if not self._dry_runs_only:
            self.log.info("Worker running in dry-runs only mode. Skipping updating metadata.")
            return

        self._update()

    def attempt_update(self) -> None:
        """Check if update of given packages will break project."""
        self.log.debug("Changing state to {state}.".format(state=States.ATTEMPTING_UPDATE.value))
        self.trigger(Triggers.TO_UPDATE_PGS.value)
        self.update_celery_state(States.ATTEMPTING_UPDATE.value)

        try:
            self._attempt_update()
        except Exception:
            self.update_successful = False
            self.log.exception("Attempt to update requirements has failed.")
            self._rollback_requirements_desired_versions()
        else:
            self.update_successful = True

    def commit_changes(self) -> None:
        """Commit changes to given project."""
        self.log.debug("Changing state to {state}.".format(state=States.COMMITTING_CHANGES.value))
        self.trigger(Triggers.TO_COMMIT.value)
        self.update_celery_state(States.COMMITTING_CHANGES.value)
        if not self.update_successful:
            self.log.debug("Requirements update was not successful, will not commit changes.")
            return

        if not self._dry_runs_only:
            self.log.info("Worker running in dry-runs only mode. Skipping committing changes.")
            return

        self._commit_changes()

    def push_changes(self) -> None:
        """Send changes to original repository as push / gerrit patch / github pull request."""
        self.log.debug("Changing state to {state}.".format(state=States.PUSHING_CHANGES.value))
        self.trigger(Triggers.TO_PUSH_CHANGES.value)
        self.update_celery_state(States.PUSHING_CHANGES.value)

        if not self._dry_runs_only:
            self.log.info("Worker running in dry-runs only mode. Skipping pushing changes.")
            return

        project_flavour = self.project_details.git_repository.flavour.casefold()
        self.log.debug("{flavour} repository type detected", project_flavour)
        if project_flavour == ProjectFlavour.GIT:
            self.log.debug("Attempting to push changes")
            self._git_push()
            return

        if project_flavour == ProjectFlavour.GITHUB:
            self.log.debug("Attempting to push changes")
            self._git_push()
            self.log.debug("Attempting to create github pull request")
            self._pull_request()
            return

        if project_flavour == ProjectFlavour.GERRIT:
            self.log.debug("Attempting to create gerrit patch")
            self._git_review()
            return

    def success(self) -> None:
        """Signify that processing of given request has succeeded."""
        self.log.debug("Changing state to {state}.".format(state=States.SUCCESS.value))
        self.trigger(Triggers.TO_SUCCESS.value)
        self.update_celery_state(States.SUCCESS.value)

    def trigger(self, transition_trigger: str) -> None:
        """This will be overridden by transitions.Machine"""

    def _save_packages_with_locked_versions(self) -> None:
        """Save ids of requirements which had pinned versions before processing.

        This is needed due to 'rollback' logic if update does not succeed.
        """
        # There is something weird with mypy here - need to investigate later
        self.log.debug("Attempting to save requirements which are pinned.")
        self._locked_packages_ids = frozenset(
            requirement.id for requirement in chain(*(  # type: ignore
                requirement_file.requirements for requirement_file in self.project_details.requirements_files
            ))
            if requirement.desired_version  # type: ignore
        )

    def _rollback_requirements_desired_versions(self):
        """Reset requirements 'desired_versions' if they were not set before this update run."""
        for requirements_file in self.project_details.requirements_files:
            self.log.debug("Rolling back requirements of '{file}'".format(
                file=requirements_file.path
            ))
            for requirement in requirements_file.requirements:
                if requirement.id in self._locked_packages_ids:
                    continue

                requirement.desired_version = ""

    @property
    def _dry_runs_only(self) -> bool:
        """Indicates if worker should attempt to commit and push changes made."""
        configuration: ConfigParser = load_config_file()
        return configuration.getboolean(section="pipwatch-worker", option="dry_runs_only", fallback=False)  # noqa: E501
