"""This module contains logic for returning API status."""
from flask_restplus import Namespace, Resource, fields

status_namespace = Namespace("status", description="Check if API is responsive.")  # pylint: disable=invalid-name
status_representation = status_namespace.model("Status", {  # pylint: disable=invalid-name
    "status": fields.String(required=True, description="Current API status (i.e. 'OK)'")
})


@status_namespace.route("/")
class Status(Resource):
    """Resource responsible for returning api status."""
    @status_namespace.doc("get_status")
    @status_namespace.marshal_with(status_representation)
    def get(self):  # pylint: disable=no-self-use
        """Return api status."""
        return {"status": "OK"}
