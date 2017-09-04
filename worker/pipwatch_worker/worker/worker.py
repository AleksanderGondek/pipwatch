"""To be defined."""
from logging import getLogger, Logger  # noqa: F401 Imported for type definition

from transitions import Machine

from pipwatch_worker.worker.states import WorkerStates, WORKER_STATE_TRANSITIONS


class Worker:
    """To be defined."""

    def __init__(self, logger: Logger = None) -> None:
        """To be defined."""
        self.log: Logger = logger or getLogger(__name__)
        self.state_machine = Machine(
            model=self,
            states=[state.value for state in WorkerStates],
            initial=WorkerStates.INITIALIZING.value,
            transitions=WORKER_STATE_TRANSITIONS
        )
