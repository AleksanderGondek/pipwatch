"""This module should contain datastores used to work on database."""

from typing import Dict, Generic, List, Optional, TypeVar

from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy

from pipwatch_api.datastore.models import Tag


T = TypeVar("T")


class DefaultStore(Generic[T]):
    """Generic datastore which can be used to work on any entity in database."""

    COLUMNS_TO_IGNORE: List[str] = ["id"]

    def __init__(self, model: T = None, database: SQLAlchemy = None) -> None:
        """
        Initialize datastore instance.

        :param model: SQLAlchemy entity model which datastore will work upon (table).
        :param database: SQLAlchemy instance which should be used to connect to database.
        """
        self.model: T = model
        self.database: SQLAlchemy = database

    def _naive_get_columns_names(self) -> List[str]:
        """Return list of keys that model object instance should contain."""
        return [name for name in self.model.__table__.columns.keys() if name not in self.COLUMNS_TO_IGNORE]

    def _additional_document_handler(self, entity: T = None, document: Dict = None):
        """
        This method can be overridden to easily extend store create and update functions.

        :param entity: SQLAlchemy entity model instance which is currently being handled.
        :param document: dictionary which represents user request for given model.
        """
        pass

    def create(self, document: Dict = None) -> T:
        """Create new document and save it to database."""
        new_instance: T = self.model()
        for column_name in self._naive_get_columns_names():
            passed_in_value: str = document.get(column_name, "")
            if not passed_in_value:
                continue

            setattr(new_instance, column_name, passed_in_value)

        self._additional_document_handler(entity=new_instance, document=document)

        self.database.session.add(new_instance)
        self.database.session.commit()
        return new_instance

    def read(self, document_id: int = -1) -> Optional[T]:
        """Attempt to retrieve document with given id from database."""
        try:
            return self.model.query.filter(self.model.id == document_id).one()
        except NoResultFound:
            return None

    def read_all(self) -> List[T]:
        """Retrieve all instances of model from database.."""
        return self.model.query.all()

    def update(self, document_id: int = -1, document: Dict = None) -> Optional[T]:
        """Attempt to update document with given id in database."""
        document_from_db: T = self.read(document_id=document_id)
        if not document_from_db:
            return None

        for column_name in self._naive_get_columns_names():
            passed_in_value: str = document.get(column_name, "")
            if not passed_in_value:
                continue

            setattr(document_from_db, column_name, passed_in_value)

        self._additional_document_handler(entity=document_from_db, document=document)

        self.database.session.add(document_from_db)
        self.database.session.commit()
        return document_from_db

    def delete(self, document_id: int = -1) -> None:
        """Delete document with given id from database."""
        document_to_be_removed: T = self.read(document_id=document_id)
        if not document_to_be_removed:
            return

        self.database.session.delete(document_to_be_removed)
        self.database.session.commit()


class ProjectStore(DefaultStore):
    """Datastore that should be used for CRUD operations on 'pipwatch_api.datastore.models.Project'."""

    COLUMNS_TO_IGNORE: List[str] = ["id", "tags"]

    def _additional_document_handler(self, entity: T = None, document: Dict = None):
        """
        Persist changes made to project tags.

        This method will make sure that any tags removed from project model will be also untagged in database,
        and any tags added to model, will also be tagged.
        """
        # Tag names are unique in table
        tag_names_from_entity = {tag.name for tag in entity.tags}
        tag_names_from_document = {tag.get("name", "") for tag in document.get("tags", []) if tag.get("name", "")}
        if not tag_names_from_entity and not tag_names_from_document:
            return

        tag_names_to_add = tag_names_from_document - tag_names_from_entity
        try:
            tags_to_add = Tag.query.filter(Tag.name.in_(tag_names_to_add)).all()
        except NoResultFound:
            tags_to_add = []

        for tag in tags_to_add:
            entity.tags.append(tag)

        entity.tags = [tag for tag in entity.tags if tag.name in tag_names_from_document]
