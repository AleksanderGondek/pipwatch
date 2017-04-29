"""This module should contain datastores used to work on database."""

from typing import Dict, List

from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import Model, SQLAlchemy


class DefaultStore:
    """Generic datastore which can be used to work on any entity in database."""

    def __init__(self, model: Model = None, database: SQLAlchemy = None) -> None:
        """
        Initialize datastore instance.

        :param model: SQLAlchemy entity model which datastore will work upon (table). 
        :param database: SQLAlchemy instance which should be used to connect to database.
        """
        self.model = model
        self.database = database

    def _naive_get_columns_names(self) -> List[str]:
        """Return list of keys that model object instance should contain."""
        return [name for name in self.model.__table__.columns.keys() if name != "id"]

    def create(self, document: Dict = None):
        """Create new document and save it to database."""
        new_instance = self.model()
        for column_name in self._naive_get_columns_names():
            passed_in_value = document.get(column_name, None)
            if not passed_in_value:
                continue

            setattr(new_instance, column_name, passed_in_value)

        self.database.session.add(new_instance)
        self.database.session.commit()
        return new_instance

    def read(self, document_id: int = -1):
        """Attempt to retrieve document with given id from database."""
        try:
            return self.model.query.filter(self.model.id == document_id).one()
        except NoResultFound:
            return None

    def read_all(self):
        """Retrieve all instances of model from database.."""
        return self.model.query.all()

    def update(self, document_id: int = -1, document: Dict = None):
        """Attempt to update document with given id in database."""
        document_from_db = self.read(document_id=document_id)
        if not document_from_db:
            return None

        for column_name in self._naive_get_columns_names():
            passed_in_value = document.get(column_name, None)
            if not passed_in_value:
                continue

            setattr(document_from_db, column_name, passed_in_value)

        self.database.session.add(document_from_db)
        self.database.session.commit()
        return document_from_db

    def delete(self, document_id: int = -1):
        """Delete document with given id from database."""
        document_to_be_removed = self.read(document_id=document_id)
        if not document_to_be_removed:
            return

        self.database.session.delete(document_to_be_removed)
        self.database.session.commit()
