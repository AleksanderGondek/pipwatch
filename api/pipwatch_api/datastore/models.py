"""This module contains data representation definitions."""

# pylint: disable=no-member,too-few-public-methods
from flask_sqlalchemy import SQLAlchemy


DATABASE = SQLAlchemy()


class Tag(DATABASE.Model):
    """Represents a single tag, which can be assigned to mark a project."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=60, convert_unicode=True), unique=True, nullable=False)

    def __init__(self, name: str = "") -> None:
        """Represents a single project entry."""
        self.name = name

    def __str__(self) -> str:
        """Return class instance human-friendly representation."""
        return "<Tag {0!r}>".format(self.name)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "{0}({1!r})".format(self.__class__.__module__ + "." + self.__class__.__name__, self.name)


TAGS = DATABASE.Table("tags",
                      DATABASE.Column("tag_id", DATABASE.Integer, DATABASE.ForeignKey("tag.id")),
                      DATABASE.Column("project_id", DATABASE.Integer, DATABASE.ForeignKey("project.id")))


class Namespace(DATABASE.Model):
    """Represents a single namespace, which can contain multiple projects."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=True, nullable=False)
    projects = DATABASE.relationship("Project", backref="namespace", lazy="dynamic")

    def __init__(self, name: str = "") -> None:
        """Represents a single project entry."""
        self.name = name

    def __str__(self) -> str:
        """Return class representation."""
        return "<Namespace {0!r}>".format(self.name)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "{0}({1!r})".format(self.__class__.__module__ + "." + self.__class__.__name__, self.name)


class Project(DATABASE.Model):
    """Represents a single project entry."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=False, nullable=False)
    url = DATABASE.Column(DATABASE.String(length=400, convert_unicode=True), unique=True, nullable=False)

    namespace_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("namespace.id"))

    tags = DATABASE.relationship("Tag", secondary=TAGS, backref=DATABASE.backref("projects", lazy="dynamic"))
    requirements_files = DATABASE.relationship("RequirementsFile", backref="project", lazy="dynamic")

    def __init__(self, name: str = "", namespace: str = "", url: str = "", namespace_id: int = "") -> None:
        """Initialize class instance."""
        self.name = name
        self.namespace = namespace
        self.url = url

        self.namespace_id = namespace_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<Project {1!r} from {0!r}>".format(self.namespace, self.name)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "{0}({1!r},{2!r})".format(self.__class__.__module__ + "." + self.__class__.__name__,
                                         self.name, self.namespace_id)


class RequirementsFile(DATABASE.Model):
    """Represents a single file  containing a list of items to be installed using pip install."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    full_path = DATABASE.Column(DATABASE.String(length=512, convert_unicode=True), unique=False, nullable=False)

    status = DATABASE.Column(DATABASE.String(length=30, convert_unicode=True), unique=False, nullable=False)

    project_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("project.id"))
    requirements = DATABASE.relationship("Requirement", backref="requirements_file", lazy="dynamic")

    def __init__(self, full_path: str = "", status: str = "", project_id: int = -1) -> None:
        """Initialize class instance."""
        self.full_path = full_path
        self.status = status

        self.project_id = project_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<RequirementsFile {0!r}>".format(self.full_path)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "{0}({1!r},{2!r},{3!r})".format(self.__class__.__module__ + "." + self.__class__.__name__,
                                                     self.full_path, self.status, self.project_id)


class Requirement(DATABASE.Model):
    """Represents a single package that should be installed via pip install."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=256, convert_unicode=True), unique=False, nullable=False)

    current_version = DATABASE.Column(DATABASE.String(length=20, convert_unicode=True), unique=False, nullable=False)
    desired_version = DATABASE.Column(DATABASE.String(length=20, convert_unicode=True), unique=False, nullable=False)

    status = DATABASE.Column(DATABASE.String(length=30, convert_unicode=True), unique=False, nullable=False)
    requirements_file_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("requirements_file.id"))

    def __init__(self, name: str = "", current_version: str = "",  # pylint: disable=too-many-arguments
                 desired_version: str = "", status: str = "",
                 requirements_file_id: int = -1) -> None:
        """Initialize class instance."""
        self.name = name
        self.current_version = current_version
        self.desired_version = desired_version
        self.status = status

        self.requirements_file_id = requirements_file_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<Requirement {0!r} ({1!r})>".format(self.name, self.current_version)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "{0}({1!r},{2!r},{3!r},{4!r},{5!r})".format(self.__class__.__module__ + "." +
                                                           self.__class__.__name__,
                                                           self.name,
                                                           self.current_version,
                                                           self.desired_version,
                                                           self.status,
                                                           self.requirements_file_id)
