"""This module contains unit tests for version one namespace resource."""
from pipwatch_api.namespaces.version_one import get_api_version_one


def test_get_api_version_one(mocker) -> None:
    """Should properly construct blueprint representing version one of pipwatch_api."""
    api_mock = mocker.patch("pipwatch_api.namespaces.version_one.Api", autospec=True)
    blueprint_mock = mocker.patch("pipwatch_api.namespaces.version_one.Blueprint", autospec=True)

    status_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.status_namespace", autospec=True)
    namespaces_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.namespaces_namespace", autospec=True)
    projects_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.projects_namespace", autospec=True)
    projects_updates_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.projects_updates_namespace", autospec=True)
    requirements_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.requirements_namespace", autospec=True)
    requirements_files_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.requirements_files_namespace", autospec=True)
    tags_ns_mock = mocker.patch("pipwatch_api.namespaces.version_one.tags_namespace", autospec=True)

    get_api_version_one()

    assert api_mock.return_value.add_namespace.call_count == 7
    assert api_mock.return_value.add_namespace.mock_calls == [
        mocker.call(status_ns_mock),
        mocker.call(namespaces_ns_mock),
        mocker.call(projects_ns_mock),
        mocker.call(projects_updates_ns_mock),
        mocker.call(requirements_ns_mock),
        mocker.call(requirements_files_ns_mock),
        mocker.call(tags_ns_mock)
    ]
