"""This module contains data representation definitions."""

# pylint: disable=no-member,too-few-public-methods
from flask_sqlalchemy import SQLAlchemy


DATABASE = SQLAlchemy()


class Tag(DATABASE.Model):
    """Represents a single tag, which can be assigned to mark a project."""
    name = DATABASE.Column(DATABASE.String(length=60, convert_unicode=True), primary_key=True)

    def __repr__(self):
        """Return class representation."""
        return "<Tag {0!r}".format(self.name)


TAGS = DATABASE.Table("tags",
                      DATABASE.Column("tag_name",
                                      DATABASE.String(length=60, convert_unicode=True),
                                      DATABASE.ForeignKey("tag.name")),
                      DATABASE.Column("project_id", DATABASE.Integer,
                                      DATABASE.ForeignKey("project.id")))


class Namespace(DATABASE.Model):
    """Represents a single namespace, which can contain multiple projects."""
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), primary_key=True)
    projects = DATABASE.relationship("Project", backref="namespace", lazy="dynamic")

    def __repr__(self):
        """Return class representation."""
        return "<Namespace {0!r}".format(self.name)


class Project(DATABASE.Model):
    """Represents a single project entry."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True), unique=False, nullable=False)
    url = DATABASE.Column(DATABASE.String(length=400, convert_unicode=True), unique=True, nullable=False)

    namespace_id = DATABASE.Column(DATABASE.String(length=200, convert_unicode=True),
                                   DATABASE.ForeignKey("namespace.name"))

    tags = DATABASE.relationship("Tag", secondary=TAGS, backref=DATABASE.backref("projects", lazy="dynamic"))
    requirements_files = DATABASE.relationship("requirementsfiles", backref="project", lazy="dynamic")

    def __init__(self, name: str = "", namespace: str = "", url: str = ""):
        """Initialize class instance."""
        self.name = name
        self.namespace = namespace
        self.url = url

    def __repr__(self):
        """Return class representation."""
        return "<Project {0!r} {1!r}>".format(self.namespace, self.name)


class RequirementsFile(DATABASE.Model):
    """Represents a single file  containing a list of items to be installed using pip install."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    full_path = DATABASE.Column(DATABASE.String(length=512, convert_unicode=True), unique=False, nullable=False)

    status = DATABASE.Column(DATABASE.String(length=30, convert_unicode=True), unique=False, nullable=False)

    project_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("project.id"))
    requirements = DATABASE.relationship("Requirement", backref="requirement0s_file", lazy="dynamic")

    def __repr__(self):
        """Return class representation."""
        return "<RequirementsFile {0!r}>".format(self.full_path)


class Requirement(DATABASE.Model):
    """Represents a single package that should be installed via pip install."""
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = DATABASE.Column(DATABASE.String(length=256, convert_unicode=True), unique=False, nullable=False)

    current_version = DATABASE.Column(DATABASE.String(length=20, convert_unicode=True), unique=False, nullable=False)
    desired_version = DATABASE.Column(DATABASE.String(length=20, convert_unicode=True), unique=False, nullable=False)

    status = DATABASE.Column(DATABASE.String(length=30, convert_unicode=True), unique=False, nullable=False)
    requirements_file_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("requirements_file.id"))

    def __repr__(self):
        """Return class representation."""
        return "<Requirement {0!r} ({1!r})>".format(self.name, self.current_version)
