"""This module contains logic for returning API status."""
from flask_restplus import Namespace, Resource, fields

STATUS_NAMESPACE = Namespace("common/status", description="Operations related to retrieving api status")
STATUS = STATUS_NAMESPACE.model("STATUS", {
    "status": fields.String(required=True, description="Current API status (i.e. 'OK)'")
})


@STATUS_NAMESPACE.route("/")
class Status(Resource):
    """Resource responsible for returning api status."""
    @STATUS_NAMESPACE.doc("get_status")
    @STATUS_NAMESPACE.marshal_with(STATUS)
    def get(self):  # pylint: disable=no-self-use
        """Return api status."""
        return {"status": "OK"}
