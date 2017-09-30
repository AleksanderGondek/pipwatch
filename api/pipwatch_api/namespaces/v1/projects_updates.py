"""This module contains logic for sending update-of-requirements task requests."""

from flask_restplus import Namespace, Resource

from pipwatch_api.celery_components.broker import ProjectUpdateBroker


projects_updates_namespace = Namespace(  # pylint: disable=invalid-name
    "projects-updates",
    description="Requirements update requests for given project"
)


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
        return self.updates_broker.check_task(task_id=task_id), 200
