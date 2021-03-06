"""This module contains unit tests for namespace resource."""
from functools import partial
import json

import pytest

from pipwatch_api.namespaces.v1.namespaces import namespace_repr_structure

from tests.namespaces.v1.conftest import get_model_repr
from tests.utils import JSONResponse


get_ns_repr = partial(get_model_repr, model=namespace_repr_structure, id=1, name="test_namespace")
get_ns_repr_empty = partial(get_model_repr, model=namespace_repr_structure)


def test_default_get_returns_all_namespaces(app_client, default_store_fixture, mocker) -> None:
    """Endpoint should return list of all namespaces."""
    expected_response = [get_ns_repr(), get_ns_repr(id=2)]
    default_store_fixture.read_all.return_value = expected_response
    mocker.patch("pipwatch_api.namespaces.v1.namespaces.DefaultStore", return_value = default_store_fixture)

    response: JSONResponse = app_client.get("/api/v1/namespaces/")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == expected_response


post_create_test_data = [
    (json.dumps(get_ns_repr(id=None)), "application/json", (201, "application/json", get_ns_repr())),
    ("some random text", "text", (400, "application/json", get_ns_repr_empty())),
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
    (1, get_ns_repr(), (200, "application/json", get_ns_repr(projects=None))),
    (2, None, (404, "application/json", get_ns_repr_empty(projects=None)))
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
    (1, get_ns_repr(), (get_ns_repr(), "application/json"), (200, "application/json", get_ns_repr())),
    (2,  -1, ("test", "text"), (400, "application/json", get_ns_repr_empty())),
    (32,  None, (get_ns_repr(id=-21), "application/json"), (404, "application/json", get_ns_repr_empty()))
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
