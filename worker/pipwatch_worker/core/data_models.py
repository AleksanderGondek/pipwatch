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

    SCHEMA = RequirementSchema()

    def __init__(self,  # pylint: disable=too-many-arguments
                 id: int,  # pylint: disable=redefined-builtin
                 name: str,
                 current_version: str,
                 desired_version: str,
                 status: str) -> None:
        """Initialize class instance."""
        self.id: int = id  # pylint: disable=invalid-name
        self.name: str = name
        self.current_version: str = current_version
        self.desired_version: str = desired_version
        self.status: str = status

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
    requirements = marshmallow.fields.Nested(RequirementSchema(), many=True)

    @marshmallow.post_load
    def to_requirements_file(self, data: Dict[Any, Any]) -> "RequirementsFile":  # pylint: disable=no-self-use
        """Enable deserialization straight to class instance."""
        return RequirementsFile(**data)


class RequirementsFile:
    """Represents a single file  containing a list of items to be installed using pip install."""

    SCHEMA = RequirementsFileSchema()

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
    namespace = marshmallow.fields.Str()
    name = marshmallow.fields.Str()
    requirements_files = marshmallow.fields.Nested(RequirementsFileSchema(), many=True)

    @marshmallow.post_load
    def to_project(self, data: Dict[Any, Any]) -> "Project":  # pylint: disable=no-self-use
        """Enable deserialization straight to class instance."""
        return Project(**data)


class Project:
    """Represents a single project entry."""

    SCHEMA = ProjectSchema()

    def __init__(self,
                 id: int,  # pylint: disable=redefined-builtin
                 namespace: str,
                 name: str,
                 requirements_files: List[RequirementsFile]) -> None:
        """Initialize class instance."""
        self.id: int = id  # pylint: disable=invalid-name
        self.namespace: str = namespace
        self.name: str = name

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
        return "<Project {self.name!r}>".format(self=self)

    def __repr__(self) -> str:
        """Return class instance representation."""
        return "<{class_name}({self.id!r},{self.namespace!r},{self.name!r})>".format(
            class_name=self.__class__.__module__ + "." + self.__class__.__name__,
            self=self
        )
