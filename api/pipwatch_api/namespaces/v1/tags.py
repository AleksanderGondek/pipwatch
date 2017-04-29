"""This module contains logic for handling operations on tag-related requests."""

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE
from pipwatch_api.datastore.models import Tag as TagModel
from pipwatch_api.datastore.stores import DefaultStore

tags_namespace = Namespace("tags", description="")  # pylint: disable=invalid-name
tag_representation = tags_namespace.model("Tag", {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description=""),
    "name": fields.String(required=True, description="")
})


@tags_namespace.route("/")
class Tags(Resource):
    """Resource representing tags collection."""
    def __init__(self, *args, **kwargs):
        """To be described."""
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

        created_tag = self.datastore.create(document=request.json)
        return created_tag, 201


@tags_namespace.route("/<int:tag_id>")
@tags_namespace.response(404, 'Tag not found.')
class Tag(Resource):
    """Resource representing operations on single tag."""
    def __init__(self, *args, **kwargs):
        """To be described."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=TagModel, database=DATABASE)

    @tags_namespace.marshal_with(tag_representation)
    @tags_namespace.response(200, "Tag found.")
    def get(self, tag_id: int):
        """Return tag with given id."""
        document = self.datastore.read(document_id=tag_id)
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

        received_document = request.json
        updated_document = self.datastore.update(document_id=tag_id, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, tag_id: int):
        """Delete tag with given id."""
        self.datastore.delete(document_id=tag_id)
        return None, 204
