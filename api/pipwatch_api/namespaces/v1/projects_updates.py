"""This module contains logic for sending update-of-requirements task requests."""
from typing import Dict

from celery.result import AsyncResult
from flask_restplus import Namespace, Resource

from pipwatch_api.celery_components.broker import ProjectUpdateBroker


projects_updates_namespace = Namespace(  # pylint: disable=invalid-name
    "projects-updates",
    description="Requirements update requests for given project"
)


@projects_updates_namespace.route("/")
class ProjectUpdates(Resource):
    """Resource representing all ongoing update requests."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.updates_broker = ProjectUpdateBroker()

    def get(self):
        """Return list of all currently ongoing update statuses."""
        pass


@projects_updates_namespace.route("/<int:project_id>")
class ProjectsUpdate(Resource):
    """Resource representing project requirements update request."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.updates_broker = ProjectUpdateBroker()

    def post(self, project_id: int):
        """Request update of requirements of project specified."""
        return self.updates_broker.send_update_request(project_id=project_id), 200


@projects_updates_namespace.route("/<string:task_id>")
class ProjectsUpdateStatus(Resource):
    """Resource representing requirements update task status."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.updates_broker = ProjectUpdateBroker()

    def get(self, task_id: str):
        """Return status of given update task."""
        task_result: AsyncResult = self.updates_broker.check_task(task_id=task_id)
        return self._async_result_to_dict(task_result=task_result), 200

    @staticmethod
    def _async_result_to_dict(task_result: AsyncResult) -> Dict[str, str]:
        """Pare celery AsyncResult into human-readable representation."""
        return {
            "info": repr(task_result.info),
            "state": task_result.state,
            "taskId": task_result.task_id
        }
