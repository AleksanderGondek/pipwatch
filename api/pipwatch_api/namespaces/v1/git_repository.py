"""This module contains logic for handling operations on git-repository-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, GitRepository as GitRepositoryModel
from pipwatch_api.datastore.stores import DefaultStore

git_repositories_namespace = Namespace(  # pylint: disable=invalid-name
    "git-repositories",
    description="CRUD operations on git repositories"
)
git_repository_repr_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description=""),
    "flavour": fields.String(required=True, description=""),
    "url": fields.String(required=True, description="")
}
git_repository_repr = git_repositories_namespace.model(  # pylint: disable=invalid-name
    "GitRepository", git_repository_repr_structure
)


@git_repositories_namespace.route("/")
class GitRepositories(Resource):
    """Resource representing git repositories collection."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=GitRepositoryModel, database=DATABASE)

    @git_repositories_namespace.marshal_list_with(git_repository_repr)
    def get(self):
        """Return list of all git repositories."""
        return self.datastore.read_all()

    @git_repositories_namespace.doc("create_git_repository")
    @git_repositories_namespace.expect(git_repository_repr)
    @git_repositories_namespace.marshal_with(git_repository_repr, code=201)
    def post(self):
        """Create a new git repository."""
        if not request.json:
            return None, 400

        created_git_repository: GitRepositoryModel = self.datastore.create(document=request.json)
        return created_git_repository, 201


@git_repositories_namespace.route("/<int:git_repo_id>")
@git_repositories_namespace.response(404, "Git repository not found.")
class GitRepository(Resource):
    """Resource representing operations on single git repository."""
    def __init__(self, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        self.datastore = DefaultStore(model=GitRepositoryModel, database=DATABASE)

    @git_repositories_namespace.marshal_with(git_repository_repr)
    @git_repositories_namespace.response(200, "Git repository found.")
    def get(self, git_repo_id: int):
        """Return git repository with given id."""
        document: GitRepositoryModel = self.datastore.read(document_id=git_repo_id)
        if not document:
            return None, 404

        return document, 200

    @git_repositories_namespace.expect(git_repository_repr)
    @git_repositories_namespace.marshal_with(git_repository_repr, code=200)
    @git_repositories_namespace.response(400, "Invalid request.")
    def put(self, git_repo_id: int):
        """Update git repository with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: GitRepositoryModel = self.datastore.update(
            document_id=git_repo_id, document=received_document
        )

        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(self, git_repo_id: int):
        """Delete git repository with given id."""
        self.datastore.delete(document_id=git_repo_id)
        return None, 204
