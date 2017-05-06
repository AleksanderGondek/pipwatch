"""This module contains logic for handling operations on project-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, RequirementsFile, Tag
from pipwatch_api.datastore.models import Project as ProjectModel
from pipwatch_api.datastore.stores import NestedDocument, WithNestedDocumentsStore

from pipwatch_api.namespaces.v1.requirements_files import requirements_file_simple_repr_structure
from pipwatch_api.namespaces.v1.tags import tag_representation_structure


TagNestedDocument = NestedDocument("tags", Tag ,"name")
RequirementsFilesNestedDocument = NestedDocument("requirements_files", RequirementsFile, "id")


projects_namespace = Namespace("projects", description="")  # pylint: disable=invalid-name
tag_representation = projects_namespace.model("Tag", tag_representation_structure)  # pylint: disable=invalid-name
project_representation_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description=""),
    "name": fields.String(required=True, description=""),
    "url": fields.String(required=True, description=""),
    "namespace_id": fields.Integer(attribute="namespace.id"),
    "namespace": fields.String(attribute="namespace.name"),
    "tags": fields.List(fields.Nested(tag_representation))
}
project_representation = projects_namespace.model("Project",  # pylint: disable=invalid-name
                                                  project_representation_structure)
requirements_file_simple_repr = projects_namespace.model("RequirementsFile",  # pylint: disable=invalid-name
                                                         requirements_file_simple_repr_structure)
project_repr_req_files = projects_namespace.inherit("Project with requirements files",  # pylint: disable=invalid-name
                                                    project_representation, {
                                                        "requirements_files": fields.List(
                                                            fields.Nested(requirements_file_simple_repr)
                                                        )
                                                    })


@projects_namespace.route("/")
class Projects(Resource):
    """Resource representing projects collection."""
    def __init__(self, *args, **kwargs):
        """To be described."""
        super().__init__(*args, **kwargs)
        self.datastore = WithNestedDocumentsStore(model=ProjectModel, database=DATABASE,
                                                  nested_documents_specs=[TagNestedDocument,
                                                                          RequirementsFilesNestedDocument])

    @projects_namespace.marshal_list_with(project_representation)
    def get(self):
        """Return list of all projects."""
        return self.datastore.read_all()

    @projects_namespace.doc("create_project")
    @projects_namespace.expect(project_repr_req_files)
    @projects_namespace.marshal_with(project_repr_req_files, code=201)
    def post(self):
        """Create a new project."""
        if not request.json:
            return None, 400

        created_document: ProjectModel = self.datastore.create(document=request.json)
        return created_document, 201


@projects_namespace.route("/<int:project_id>")
@projects_namespace.response(404, "Project not found.")
class Project(Resource):
    """Resource representing operations on single project."""
    def __init__(self, *args, **kwargs):
        """To be described."""
        super().__init__(*args, **kwargs)
        self.datastore = WithNestedDocumentsStore(model=ProjectModel, database=DATABASE,
                                                  nested_documents_specs=[TagNestedDocument,
                                                                          RequirementsFilesNestedDocument])

    @projects_namespace.marshal_with(project_repr_req_files)
    @projects_namespace.response(200, "Namespace found.")
    def get(self, project_id: int):
        """Return project with given id."""
        document: ProjectModel = self.datastore.read(document_id=project_id)
        if not document:
            return None, 404

        return document, 200

    @projects_namespace.expect(project_repr_req_files)
    @projects_namespace.marshal_with(project_repr_req_files, code=200)
    @projects_namespace.response(400, "Invalid request.")
    def put(self, project_id: int):
        """Update project with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: ProjectModel = self.datastore.update(document_id=project_id, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, project_id: int):
        """Delete project with given id."""
        self.datastore.delete(document_id=project_id)
        return None, 204
