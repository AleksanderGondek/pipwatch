"""This module contains logic responsible for creation of API v1 blueprint."""
from flask import Blueprint
from flask_restplus import Api

from pipwatch_api.namespaces.v1.status import status_namespace
from pipwatch_api.namespaces.v1.tags import tags_namespace
from pipwatch_api.version import VERSION


def get_api_version_one() -> Blueprint:
    """Return API blueprint of version 1.X, with all namespaces registered"""
    version_one_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api_version_one = Api(version_one_blueprint,
                          title="Pipwatch API",
                          version=VERSION,
                          description="API for interacting witch pipwatch")

    api_version_one.add_namespace(status_namespace)
    api_version_one.add_namespace(tags_namespace)

    return version_one_blueprint
