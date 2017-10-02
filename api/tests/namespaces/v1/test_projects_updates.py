"""This module contains unit tests for projects-updates resource."""

from tests.namespaces.v1.conftest import AsyncResultMock
from tests.utils import JSONResponse


def test_post_creates_a_new_task(app_client, mocker) -> None:
    """Endpoint should fire project update task."""
    update_broker_mock = mocker.patch("pipwatch_api.namespaces.v1.projects_updates.ProjectUpdateBroker")
    update_broker_mock.return_value.send_update_request.return_value = "celery-task-id"

    response: JSONResponse = app_client.post("/api/v1/projects-updates/1", content_type="application/json")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == "celery-task-id"


def test_get_task_status(app_client, mocker) -> None:
    """Endpoint should return project update task status."""
    update_broker_mock = mocker.patch("pipwatch_api.namespaces.v1.projects_updates.ProjectUpdateBroker")
    update_broker_mock.return_value.check_task.return_value = AsyncResultMock("test-info", "test-state", "test-task-id")

    response: JSONResponse = app_client.get("/api/v1/projects-updates/test-task-id", content_type="application/json")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == {
        "info": "'test-info'",
        "state": "test-state",
        "taskId": "test-task-id"
    }
