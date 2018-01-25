"""This module contains logic for handling operations on tag-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, Tag as TagModel
from pipwatch_api.datastore.stores import DefaultStore

tags_namespace = Namespace(  # pylint: disable=invalid-name
    "tags",
    description="CRUD operations on tags"
)
tag_representation_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description="Id of given tag, unique across the database"),
    "name": fields.String(required=True, description="Name of given tag (i.e. 'awesome-sauce')")
}
tag_representation = tags_namespace.model("Tag", tag_representation_structure)  # pylint: disable=invalid-name


@tags_namespace.route("/")
class Tags(Resource):
    """Resource representing tags collection."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=TagModel, database=DATABASE)

    @tags_namespace.marshal_list_with(tag_representation)
    def get(self):
        """Return list of all tags."""
        return self.datastore.read_all()

    @tags_namespace.doc("create_tag")
    @tags_namespace.expect(tag_representation)
    @tags_namespace.marshal_with(tag_representation, code=201)
    def post(self):
        """Create a new tag."""
        if not request.json:
            return None, 400

        created_tag: TagModel = self.datastore.create(document=request.json)
        return created_tag, 201


@tags_namespace.route("/<int:tag_id>")
@tags_namespace.response(404, "Tag not found.")
class Tag(Resource):
    """Resource representing operations on single tag."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=TagModel, database=DATABASE)

    @tags_namespace.marshal_with(tag_representation)
    @tags_namespace.response(200, "Tag found.")
    def get(self, tag_id: int):
        """Return tag with given id."""
        document: TagModel = self.datastore.read(document_id=tag_id)
        if not document:
            return None, 404

        return document, 200

    @tags_namespace.expect(tag_representation)
    @tags_namespace.marshal_with(tag_representation, code=200)
    @tags_namespace.response(400, "Invalid request.")
    def put(self, tag_id: int):
        """Update tag with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: TagModel = self.datastore.update(document_id=tag_id, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, tag_id: int):
        """Delete tag with given id."""
        self.datastore.delete(document_id=tag_id)
        return None, 204
