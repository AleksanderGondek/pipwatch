"""This module contains logic for handling operations on namespace-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace as FlaskNamespace
from flask_restplus import Resource, fields

from pipwatch_api.datastore.models import DATABASE
from pipwatch_api.datastore.models import Namespace as NamespaceModel
from pipwatch_api.datastore.stores import DefaultStore

from pipwatch_api.namespaces.v1.projects import project_representation_structure

namespaces_namespace = FlaskNamespace("namespaces", description="")  # pylint: disable=invalid-name

project_repr = namespaces_namespace.model("Project", project_representation_structure)  # pylint: disable=invalid-name
namespace_repr = namespaces_namespace.model("Namespace", {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description=""),
    "name": fields.String(required=True, description="")
})
namespace_repr_detailed = namespaces_namespace.inherit("Namespace with projects",  # pylint: disable=invalid-name
                                                       namespace_repr, {
                                                           "projects": fields.List(fields.Nested(project_repr))
                                                       })


@namespaces_namespace.route("/")
class Namespaces(Resource):
    """Resource representing namespaces collection."""
    def __init__(self, *args, **kwargs):
        """To be described."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=NamespaceModel, database=DATABASE)

    @namespaces_namespace.marshal_list_with(namespace_repr)
    def get(self):
        """Return list of all namespaces."""
        return self.datastore.read_all()

    @namespaces_namespace.doc("create_namespace")
    @namespaces_namespace.expect(namespace_repr)
    @namespaces_namespace.marshal_with(namespace_repr, code=201)
    def post(self):
        """Create a new namespace."""
        if not request.json:
            return None, 400

        created_document: NamespaceModel = self.datastore.create(document=request.json)
        return created_document, 201


@namespaces_namespace.route("/<int:namespace_id>")
@namespaces_namespace.response(404, "Namespace not found.")
class Namespace(Resource):
    """Resource representing operations on single namespace."""
    def __init__(self, *args, **kwargs):
        """To be described."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=NamespaceModel, database=DATABASE)

    @namespaces_namespace.marshal_with(namespace_repr_detailed)
    @namespaces_namespace.response(200, "Namespace found.")
    def get(self, namespace_id: int):
        """Return namespace with given id."""
        document: NamespaceModel = self.datastore.read(document_id=namespace_id)
        if not document:
            return None, 404

        return document, 200

    @namespaces_namespace.expect(namespace_repr)
    @namespaces_namespace.marshal_with(namespace_repr, code=200)
    @namespaces_namespace.response(400, "Invalid request.")
    def put(self, namespace_id: int):
        """Update namespace with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: NamespaceModel = self.datastore.update(document_id=namespace_id, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, namespace_id: int):
        """Delete namespace with given id."""
        self.datastore.delete(document_id=namespace_id)
        return None, 204
