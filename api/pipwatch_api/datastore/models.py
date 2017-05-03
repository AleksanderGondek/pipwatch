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
        return "<Tag {self.name!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "<{class_name}({self.name!r})>".format(
            class_name=self.__class__.__module__ + "." + self.__class__.__name__,
            self=self
        )


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
        return "<Namespace {self.name!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "<{class_name}({self.name!r})>".format(
            class_name=self.__class__.__module__ + "." + self.__class__.__name__,
            self=self
        )


class Project(DATABASE.Model):
    """Represents a single project entry."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=False, nullable=False)
    url = DATABASE.Column(DATABASE.String(length=400, convert_unicode=True), unique=True, nullable=False)

    namespace_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("namespace.id"))

    tags = DATABASE.relationship("Tag", secondary=TAGS, backref=DATABASE.backref("projects", lazy="dynamic"))
    requirements_files = DATABASE.relationship("RequirementsFile", backref="project", lazy="dynamic")

    def __init__(self, name: str = "", url: str = "", namespace_id: int = -1) -> None:
        """Initialize class instance."""
        self.name = name
        self.url = url

        if namespace_id >= 0:
            self.namespace_id = namespace_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<Project {self.name!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "<{class_name}({self.name!r},{self.namespace_id!r})>".format(
            class_name=self.__class__.__module__ + "." + self.__class__.__name__,
            self=self
        )


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

        if project_id >= 0:
            self.project_id = project_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<RequirementsFile {self.full_path!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return (
            "<{class_name}("
            "{self.full_path!r},"
            "{self.status!r},"
            "{self.project_id!r})"
            ">".format(
                class_name=self.__class__.__module__ + "." + self.__class__.__name__,
                self=self
            )
        )


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

        if requirements_file_id >= 0:
            self.requirements_file_id = requirements_file_id

    def __str__(self) -> str:
        """Return class representation."""
        return "<Requirement {self.name!r}({self.current_version!r})>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return (
            "<{class_name}("
            "{self.name!r},"
            "{self.current_version!r},"
            "{self.desired_version!r},"
            "{self.status!r},"
            "{self.requirements_file_id!r})"
            ">".format(
                class_name=self.__class__.__module__ + "." + self.__class__.__name__,
                self=self
            )
        )