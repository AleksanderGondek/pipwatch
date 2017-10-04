"""This module contains logic responsible for starting the pipwatch worker tasks via cli."""

import json
from logging import getLogger, Logger  # noqa: F401 Imported for type definition
import sys

from pipwatch_worker.celery_components.application import app
from pipwatch_worker.core.configuration import configure_logger


def main() -> None:
    """Function to start the given celery task."""
    configure_logger()
    log: Logger = getLogger(__name__)

    if len(sys.argv) <= 1:
        log.info("Please provide name of task to run.")
        sys.exit(1)

    _, task_name, task_args, *_ = sys.argv  # type: ignore
    log.info("Sending task %s.", task_name)
    log.info("Task args (should be json): %s.", task_args)

    result_async = app.send_task(task_name, args=json.loads(task_args), kwargs=None)
    log.info("Waiting for task results.")
    result_async.get()

    log.info("Task finished.")
    sys.exit(0)


if __name__ == "__main__":
    main()
