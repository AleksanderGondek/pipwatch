"""This module contains logic responsible for creation of API v1 blueprint."""
from flask import Blueprint
from flask_restplus import Api

from pipwatch_api.namespaces.v1.namespaces import namespaces_namespace
from pipwatch_api.namespaces.v1.projects import projects_namespace
from pipwatch_api.namespaces.v1.projects_updates import projects_updates_namespace
from pipwatch_api.namespaces.v1.requirements import requirements_namespace
from pipwatch_api.namespaces.v1.requirements_files import requirements_files_namespace
from pipwatch_api.namespaces.v1.status import status_namespace
from pipwatch_api.namespaces.v1.tags import tags_namespace
from pipwatch_api.version import VERSION


def get_api_version_one() -> Blueprint:
    """Return API blueprint of version 1.X, with all namespaces registered"""
    version_one_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api_version_one = Api(version_one_blueprint,
                          title="Pipwatch API",
                          version=VERSION,
                          description="Restful interface for interacting with pipwatch")

    api_version_one.add_namespace(status_namespace)
    api_version_one.add_namespace(namespaces_namespace)
    api_version_one.add_namespace(projects_namespace)
    api_version_one.add_namespace(projects_updates_namespace)
    api_version_one.add_namespace(requirements_namespace)
    api_version_one.add_namespace(requirements_files_namespace)
    api_version_one.add_namespace(tags_namespace)

    return version_one_blueprint
