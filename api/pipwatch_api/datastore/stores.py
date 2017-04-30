"""This module should contain datastores used to work on database."""

from typing import Dict, Generic, List, Optional, TypeVar

from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy


T = TypeVar("T")


class DefaultStore(Generic[T]):
    """Generic datastore which can be used to work on any entity in database."""

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
        return [name for name in self.model.__table__.columns.keys() if name != "id"]

    def create(self, document: Dict = None) -> T:
        """Create new document and save it to database."""
        new_instance: T = self.model()
        for column_name in self._naive_get_columns_names():
            passed_in_value: str = document.get(column_name, "")
            if not passed_in_value:
                continue

            setattr(new_instance, column_name, passed_in_value)

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
