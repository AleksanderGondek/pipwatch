"""This module contains logic for handling operations on requests related to requirements."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, Requirement as RequirementModel
from pipwatch_api.datastore.stores import DefaultStore


requirements_namespace = Namespace(  # pylint: disable=invalid-name
    "requirements",
    description="CRUD operations on requirements"
)
requirement_repr_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description="Id of given requirement, unique across the database"),
    "name": fields.String(required=True, description="Name of given package (i.e. 'requests')"),
    "current_version": fields.String(required=True, description="Version of package as present in requirements file"),
    "desired_version": fields.String(required=True, description="Desired version of given package"),
    "status": fields.String(required=True, description=""),
    "requirements_file_id": fields.Integer(required=True, attribute="requirements_file.id")
}
requirement_repr = requirements_namespace.model(  # pylint: disable=invalid-name
    "Requirement",
    requirement_repr_structure
)


@requirements_namespace.route("/")
class Requirements(Resource):
    """Resource representing requirements collection."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=RequirementModel, database=DATABASE)

    @requirements_namespace.marshal_list_with(requirement_repr)
    def get(self):
        """Return list of all requirements."""
        return self.datastore.read_all()

    @requirements_namespace.doc("create_requirement")
    @requirements_namespace.expect(requirement_repr)
    @requirements_namespace.marshal_with(requirement_repr, code=201)
    def post(self):
        """Create a new requirement."""
        if not request.json:
            return None, 400

        created_document: RequirementModel = self.datastore.create(document=request.json)
        return created_document, 201


@requirements_namespace.route("/<int:requirement_id>")
@requirements_namespace.response(404, "Requirement not found.")
class Requirement(Resource):
    """Resource representing operations on single requirement."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=RequirementModel, database=DATABASE)

    @requirements_namespace.marshal_with(requirement_repr)
    @requirements_namespace.response(200, "Requirement found.")
    def get(self, requirement_id: int):
        """Return requirement with given id."""
        document: RequirementModel = self.datastore.read(document_id=requirement_id)
        if not document:
            return None, 404

        return document, 200

    @requirements_namespace.expect(requirement_repr)
    @requirements_namespace.marshal_with(requirement_repr, code=200)
    @requirements_namespace.response(400, "Invalid request.")
    def put(self, requirement_id: int):
        """Update requirement with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: RequirementModel = self.datastore.update(
            document_id=requirement_id, document=received_document
        )
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, requirement_id: int):
        """Delete requirement with given id."""
        self.datastore.delete(document_id=requirement_id)
        return None, 204
