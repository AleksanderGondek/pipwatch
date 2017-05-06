"""This module contains logic for handling operations on requests related to requirements files."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE
from pipwatch_api.datastore.models import RequirementsFile as RequirementsFileModel
from pipwatch_api.datastore.stores import DefaultStore

from pipwatch_api.namespaces.v1.requirements import requirement_repr_structure


requirements_files_namespace = Namespace("requirements-files",  # pylint: disable=invalid-name
                                         description="CRUD operations on requirements-files")
requirements_file_simple_repr_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description=""),
    "full_path": fields.String(required=True, description=""),
    "status": fields.String(required=True, description=""),
    "project_id": fields.Integer(required=True, attribute="project.id"),
}
requirements_file_simple_repr = requirements_files_namespace.model("RequirementsFile",  # pylint: disable=invalid-name
                                                                   requirements_file_simple_repr_structure)
requirement_repr = requirements_files_namespace.model("Requirement",  # pylint: disable=invalid-name
                                                      requirement_repr_structure)
requirements_file_repr = requirements_files_namespace.inherit("Reqs-file detailed",  # pylint: disable=invalid-name
                                                              requirements_file_simple_repr,
                                                              {
                                                                  "requirements": fields.List(
                                                                      fields.Nested(requirement_repr)
                                                                  )
                                                              })


@requirements_files_namespace.route("/")
class RequirementsFiles(Resource):
    """Resource representing requirements-files collection."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=RequirementsFileModel, database=DATABASE)

    @requirements_files_namespace.marshal_list_with(requirements_file_simple_repr)
    def get(self):
        """Return list of all requirements-files."""
        return self.datastore.read_all()

    @requirements_files_namespace.doc("create_requirements_file")
    @requirements_files_namespace.expect(requirements_file_repr)
    @requirements_files_namespace.marshal_with(requirements_file_repr, code=201)
    def post(self):
        """Create a new requirements-file."""
        if not request.json:
            return None, 400

        created_document: RequirementsFileModel = self.datastore.create(document=request.json)
        return created_document, 201


@requirements_files_namespace.route("/<int:requirements_file_id>")
@requirements_files_namespace.response(404, "Requirements-file not found.")
class RequirementsFile(Resource):
    """Resource representing operations on single requirement."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=RequirementsFileModel, database=DATABASE)

    @requirements_files_namespace.marshal_with(requirements_file_repr)
    @requirements_files_namespace.response(200, "Requirements-file found.")
    def get(self, requirements_file_id: int):
        """Return requirements-file with given id."""
        document: RequirementsFileModel = self.datastore.read(document_id=requirements_file_id)
        if not document:
            return None, 404

        return document, 200

    @requirements_files_namespace.expect(requirements_file_repr)
    @requirements_files_namespace.marshal_with(requirements_file_repr, code=200)
    @requirements_files_namespace.response(400, "Invalid request.")
    def put(self, requirements_file_id: int):
        """Update requirements-file with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: RequirementsFileModel = self.datastore.update(
            document_id=requirements_file_id, document=received_document
        )
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, requirements_file_id: int):
        """Delete requirements-file with given id."""
        self.datastore.delete(document_id=requirements_file_id)
        return None, 204
