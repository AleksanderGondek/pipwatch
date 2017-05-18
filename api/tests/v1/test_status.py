"""This module contains unit tests for status resource."""
from tests.utils import JSONResponse


def test_status_should_return_ok(app_client) -> None:
    """Endpoint should return json representing 'ok' status."""
    response: JSONResponse = app_client.get("/api/v1/status/")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == {"status": "OK"}
