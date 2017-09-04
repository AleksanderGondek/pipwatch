"""This module contains pipwatch worker definition."""

from logging import getLogger, Logger  # noqa: F401 Imported for type definition

from transitions import Machine

from pipwatch_worker.worker.states import WorkerStates, WORKER_STATE_TRANSITIONS


class Worker:
    """Responsible for checking and updating python packages in given project."""

    def __init__(self, logger: Logger = None) -> None:
        """Initialize worker instance."""
        self.log: Logger = logger or getLogger(__name__)
        self.state_machine = Machine(
            model=self,
            states=[state.value for state in WorkerStates],
            initial=WorkerStates.INITIALIZING.value,
            transitions=WORKER_STATE_TRANSITIONS
        )
