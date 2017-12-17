"""This module contains classes that represent data objects received and returned by worker."""
from typing import Any, Dict, List

import marshmallow


class RequirementSchema(marshmallow.Schema):
    """Marshmellow schema of Requirement class - allows for easy serialization/deserialization."""

    id = marshmallow.fields.Int()  # pylint: disable=invalid-name
    name = marshmallow.fields.Str()
    current_version = marshmallow.fields.Str()
    desired_version = marshmallow.fields.Str()
    status = marshmallow.fields.Str()

    @marshmallow.post_load
    def to_requirement(self, data: Dict[Any, Any]) -> "Requirement":  # pylint: disable=no-self-use
        """Enable deserialization straight to class instance."""
        return Requirement(**data)


class Requirement:
    """Represents a single package that should be installed via pip install."""

    SCHEMA = RequirementSchema(strict=True)

    def __init__(self,  # pylint: disable=too-many-arguments
                 id: int = None,  # pylint: disable=redefined-builtin
                 name: str = None,
                 current_version: str = None,
                 desired_version: str = None,
                 status: str = None) -> None:
        """Initialize class instance."""
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.current_version = current_version
        self.desired_version = desired_version
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        """Return class instance representation as dictionary."""
        return self.SCHEMA.dump(self).data

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Requirement":
        """Create class instance from dictionary."""
        return cls.SCHEMA.load(dictionary).data

    def __str__(self):
        """Return class representation."""
        return "<Requirement {self.name!r}({self.current_version!r})>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return (
            "<{class_name}("
            "{self.id!r},"
            "{self.name!r},"
            "{self.current_version!r},"
            "{self.desired_version!r},"
            "{self.status!r})"
            ">".format(
                class_name=self.__class__.__module__ + "." + self.__class__.__name__,
                self=self
            )
        )


class RequirementsFileSchema(marshmallow.Schema):
    """Marshmellow schema of RequirementsFile class - allows for easy serialization/deserialization."""

    id = marshmallow.fields.Int()  # pylint: disable=invalid-name
    path = marshmallow.fields.Str()
    status = marshmallow.fields.Str()
    requirements = marshmallow.fields.Nested(RequirementSchema, many=True)

    @marshmallow.post_load
    def to_requirements_file(self, data: Dict[Any, Any]) -> "RequirementsFile":  # pylint: disable=no-self-use
        """Enable deserialization straight to class instance."""
        return RequirementsFile(**data)


class RequirementsFile:
    """Represents a single file  containing a list of items to be installed using pip install."""

    SCHEMA = RequirementsFileSchema(strict=True)

    def __init__(self,
                 id: int,  # pylint: disable=redefined-builtin
                 path: str,
                 status: str,
                 requirements: List[Requirement]) -> None:
        """Initialize class instance."""
        self.id: int = id  # pylint: disable=invalid-name
        self.path: str = path
        self.status: str = status

        self.requirements: List[Requirement] = requirements

    def to_dict(self) -> Dict[str, Any]:
        """Return class instance representation as dictionary."""
        return self.SCHEMA.dump(self).data

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "RequirementsFile":
        """Create class instance from dictionary."""
        return cls.SCHEMA.load(dictionary).data

    def __str__(self) -> str:
        """Return class representation."""
        return "<RequirementsFile {self.path!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return (
            "<{class_name}("
            "{self.id!r},"
            "{self.path!r},"
            "{self.status!r})"
            ">".format(
                class_name=self.__class__.__module__ + "." + self.__class__.__name__,
                self=self
            )
        )


class ProjectSchema(marshmallow.Schema):
    """Marshmellow schema of Project class - allows for easy serialization/deserialization."""

    id = marshmallow.fields.Int()  # pylint: disable=invalid-name
    namespace_id = marshmallow.fields.Int()
    name = marshmallow.fields.Str()
    flavour: str = marshmallow.fields.Str(allow_none=True)
    url = marshmallow.fields.Str()
    upstream_url = marshmallow.fields.Str(allow_none=True)
    check_command = marshmallow.fields.Str()
    requirements_files = marshmallow.fields.Nested(RequirementsFileSchema, many=True)

    @marshmallow.post_load
    def to_project(self, data: Dict[Any, Any]) -> "Project":  # pylint: disable=no-self-use
        """Enable deserialization straight to class instance."""
        return Project(**data)


class Project:  # pylint: disable=too-many-instance-attributes
    """Represents a single project entry."""

    SCHEMA = ProjectSchema(strict=True)

    def __init__(self,  # pylint: disable=too-many-arguments
                 id: int,  # pylint: disable=redefined-builtin
                 namespace_id: int,
                 name: str,
                 flavour: str,
                 url: str,
                 upstream_url: str,
                 check_command: str,
                 requirements_files: List[RequirementsFile]) -> None:
        """Initialize class instance."""
        self.id: int = id  # pylint: disable=invalid-name
        self.namespace_id: int = namespace_id
        self.name: str = name
        self.flavour: str = flavour
        self.url: str = url
        self.upstream_url: str = upstream_url
        self.check_command: str = check_command

        self.requirements_files: List[RequirementsFile] = requirements_files

    def to_dict(self) -> Dict[str, Any]:
        """Return class instance representation as dictionary."""
        return self.SCHEMA.dump(self).data

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Project":
        """Create class instance from dictionary."""
        return cls.SCHEMA.load(dictionary).data

    def __str__(self) -> str:
        """Return class representation."""
        return "<Project {self.url!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "<{class_name}({self.id!r},{self.namespace_id!r}," \
               "{self.name!r},{self.flavour!r}{self.url!r}," \
               "{self.upstream_url},{self.check_command!r})>".format(
                   class_name=self.__class__.__module__ + "." + self.__class__.__name__, self=self)
