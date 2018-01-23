"""This module contains logic for returning API status."""
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.version import VERSION

status_namespace = Namespace("status", description="retrieve the api instance status.")  # pylint: disable=invalid-name
status_representation = status_namespace.model(  # pylint: disable=invalid-name
    "Status",
    {
        "status": fields.String(required=True, description="Current API status (i.e. 'OK')"),
        "version": fields.String(required=True, description="API version (i.e. '0.0.1'")
    }
)


@status_namespace.route("/")
class Status(Resource):
    """Resource responsible for returning api status and version."""
    @status_namespace.doc("get_status")
    @status_namespace.marshal_with(status_representation)
    def get(self):  # pylint: disable=no-self-use
        """Retrieve the current status and version of the api instance."""
        return {
            "status": "OK",
            "version": VERSION
        }
