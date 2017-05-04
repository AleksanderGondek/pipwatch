"""This module should contain datastores used to work on database."""

from typing import Dict, Generic, List, NamedTuple, Optional, TypeVar

from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy, Model

from pipwatch_api.datastore.models import Tag


T = TypeVar("T")


class DefaultStore(Generic[T]):
    """Generic datastore which can be used to work on any entity in database."""

    def __init__(self, model: T = None, database: SQLAlchemy = None) -> None:
        """
        Initialize datastore instance.

        :param model: SQLAlchemy entity model which datastore will work upon (table).
        :param database: SQLAlchemy instance which should be used to connect to database.
        """
        self.columns_to_ignore: List[str] = ["id"]
        self.model: T = model
        self.database: SQLAlchemy = database

    def _naive_get_columns_names(self) -> List[str]:
        """Return list of keys that model object instance should contain."""
        return [name for name in self.model.__table__.columns.keys() if name not in self.columns_to_ignore]

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


NestedDocument = NamedTuple("NestedDocument", ("property_name", str),
                            ("document_model", Model), ("differentiator_property", str))


class WithNestedDocumentsStore(DefaultStore):
    """To be described."""

    def __init__(self, model: T = None, database: SQLAlchemy = None,
                 nested_documents_specs: List[NestedDocument]=None) -> None:
        """To be described."""
        super().__init__(model=model, database=database)
        self.nested_documents_specs: List[NestedDocument] = nested_documents_specs
        self._load_nested_documents_properties_names()

    def _load_nested_documents_properties_names(self) -> None:
        """To be described."""
        for property_name, _, _ in self.nested_documents_specs:
            self.columns_to_ignore.append(property_name)

    def _persist_nested_document(self, entity: T = None, document: Dict = None,
                                 nested_doc_key: str = "", nested_doc_model: Model = None,
                                 differentiator_property: str = "") -> None:
        """To be described."""
        ids_from_entity = {getattr(nested_document, differentiator_property) for nested_document
                           in getattr(entity, nested_doc_key)
                           if getattr(nested_document, differentiator_property, None)}
        ids_from_document = {nested_document.get(differentiator_property, "") for nested_document
                             in document.get(nested_doc_key, [])
                             if nested_document.get(differentiator_property, "")}
        if not ids_from_entity and not ids_from_document:
            return

        ids_to_be_added = ids_from_document - ids_from_entity
        try:
            sub_documents_to_add = nested_doc_model.query.filter(
                getattr(nested_doc_model, differentiator_property).in_(ids_to_be_added)
            ).all()
        except NoResultFound:
            sub_documents_to_add = []

        for sub_document in sub_documents_to_add:
            getattr(entity, nested_doc_key).append(sub_document)

        setattr(entity, nested_doc_key, [sub_document for sub_document
                                         in getattr(entity, nested_doc_key, [])
                                         if getattr(sub_document, differentiator_property) in ids_from_document])


    def _additional_document_handler(self, entity: T = None, document: Dict = None):
        """To be described."""
        for nested_doc_key, nested_doc_model, differentiator_property in self.nested_documents_specs:
            self._persist_nested_document(entity=entity, document=document,
                                          nested_doc_key=nested_doc_key,
                                          nested_doc_model=nested_doc_model,
                                          differentiator_property=differentiator_property)
