"""This module contains unit tests for namespace resource."""
import json
import pytest

from tests.utils import JSONResponse


def test_default_get_returns_all_namespaces(app_client, default_store_fixture, mocker) -> None:
    """Endpoint should return list of all namespaces."""
    expected_response = [{"id": 1, "name": "test"}, {"id": 2, "name": "another_test"}]
    default_store_fixture.read_all.return_value = expected_response
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    response: JSONResponse = app_client.get("/api/v1/namespaces/")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == expected_response


post_create_test_data = [
    ("{\"name\": \"example2\"}", "application/json", (201, "application/json", {"id": 1, "name": "example2"})),
    ("some random text", "text", (400, "application/json", {"id": None, "name": None})),
]

@pytest.mark.parametrize("payload, content_type, asserts", post_create_test_data)
def test_post_creates_a_new_namespace(payload, content_type, asserts, app_client, default_store_fixture, mocker) -> None:
    """Endpoint should create new namespace and return it."""
    default_store_fixture.create.return_value = asserts[2]
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    response: JSONResponse = app_client.post("/api/v1/namespaces/", data=payload, content_type=content_type)

    assert response.status_code == asserts[0]
    assert response.content_type == asserts[1]
    assert response.json == asserts[2]


get_id_test_data = [
    (1, {"id": 1, "name": "test"}, (200, "application/json", {"id": 1, "name": "test", "projects": None})),
    (2, None, (404, "application/json", {"id": None, "name": None, "projects": None}))
]


@pytest.mark.parametrize("document_id, mock_response, asserts", get_id_test_data)
def test_get_id_returns_document(document_id, mock_response, asserts, app_client,
                                 default_store_fixture, mocker) -> None:
    """Endpoint should get a namespace with given id."""
    default_store_fixture.read.return_value = mock_response
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    response: JSONResponse = app_client.get("/api/v1/namespaces/{0}".format(document_id))

    default_store_fixture.read.assert_called_with(document_id)

    assert response.status_code == asserts[0]
    assert response.content_type == asserts[1]
    assert response.json == asserts[2]


put_test_data = [
    (1,  {"id": 1, "name": "testos"},
     ({"id": 1, "name": "testos"}, "application/json"),
     (200, "application/json", {"id": 1, "name": "testos"})),
    (2,  -1,
     ("test", "text"),
     (400, "application/json", {"id": None, "name": None})),
    (32,  None,
     ({"id": 32, "name": "not_existing"}, "application/json"),
     (404, "application/json", {"id": None, "name": None}))
]


@pytest.mark.parametrize("document_id, mock_response, payload, asserts", put_test_data)
def test_put_updates_document(document_id, mock_response, payload,
                              asserts, app_client, default_store_fixture, mocker) -> None:
    """Endpoint should update namespace with given id."""
    default_store_fixture.update.return_value = mock_response
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    response: JSONResponse = app_client.put("/api/v1/namespaces/{0}".format(document_id),
                                            data=json.dumps(payload[0]),
                                            content_type=payload[1])

    if mock_response != -1:
        default_store_fixture.update.assert_called_with(document_id, payload[0])

    assert response.status_code == asserts[0]
    assert response.content_type == asserts[1]
    assert response.json == asserts[2]


def test_delete_namespace(app_client, default_store_fixture, mocker) -> None:
    """Endpoint should create new namespace and return it."""
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    document_id = 1
    response: JSONResponse = app_client.delete("/api/v1/namespaces/{}".format(document_id))

    assert response.status_code == 204
    assert response.content_type == "application/json"
