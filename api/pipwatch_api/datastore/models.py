"""This module contains data representation definitions."""
from pipwatch_api.datastore import DATABASE


# pylint: disable=no-member,too-few-public-methods
class Project(DATABASE.Model):
    """Represents a single project entry."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=False, nullable=False)
    namespace = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=True, nullable=False)
    url = DATABASE.Column(DATABASE.String(length=400, convert_unicode=True), unique=True, nullable=False)

    def __init__(self, name: str = "", namespace: str = "", url: str = ""):
        """Initialize class instance."""
        self.name = name
        self.namespace = namespace
        self.url = url

    def __repr__(self):
        """Return class representation."""
        return "<Project {0!r} {0!r>".format(self.namespace, self.name)  # pylint: disable=bad-format-string
