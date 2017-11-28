"""This module should contain datastores used to work on database."""

from logging import getLogger, Logger
from typing import Dict, Generic, List, NamedTuple, Optional, TypeVar

from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy, Model


T = TypeVar("T", bound=Model)


class DefaultStore(Generic[T]):
    """Generic datastore which can be used to work on any entity in database."""

    def __init__(self, model: T = None, database: SQLAlchemy = None, logger: Logger = None) -> None:
        """
        Initialize datastore instance.

        :param model: SQLAlchemy entity model which datastore will work upon (table).
        :param database: SQLAlchemy instance which should be used to connect to database.
        :param logger: Logger instance which should be used to log. Optional.
        """
        self.columns_to_ignore: List[str] = ["id"]
        self.log = logger or getLogger(__name__)
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
        self.log.debug("Attempting to create new entity of '%s' from document of '%s'.",
                       type(self.model).__qualname__,
                       repr(document))
        new_instance: T = self.model()
        for column_name in self._naive_get_columns_names():
            passed_in_value: str = document.get(column_name, "")
            if not passed_in_value:
                continue

            setattr(new_instance, column_name, passed_in_value)

        self._additional_document_handler(entity=new_instance, document=document)

        self.database.session.add(new_instance)
        self.database.session.commit()
        self.log.debug("New entity created and committed.")
        return new_instance

    def read(self, document_id: int = -1) -> Optional[T]:
        """Attempt to retrieve document with given id from database."""
        self.log.debug("Attempting to find entity with id of '%s'.", str(document_id))
        try:
            return self.model.query.filter(self.model.id == document_id).one()
        except NoResultFound:
            self.log.debug("Entity with id of '%s' not found. Returning 'None'.", str(document_id))
            return None

    def read_all(self) -> List[T]:
        """Retrieve all instances of model from database.."""
        self.log.debug("Attempting to return all entities of type '%s'.", type(self.model).__qualname__)
        return self.model.query.all()

    def update(self, document_id: int = -1, document: Dict = None) -> Optional[T]:
        """Attempt to update document with given id in database."""
        self.log.debug("Attempting to update entity of '%s' with id of '%s' from document of '%s'.",
                       type(self.model).__qualname__,
                       str(document_id),
                       repr(document))
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
        self.log.debug("Entity updated and committed.")
        return document_from_db

    def delete(self, document_id: int = -1) -> None:
        """Delete document with given id from database."""
        self.log.debug("Attempting to delete entity with id of '{%s}'.", str(document_id))
        document_to_be_removed: T = self.read(document_id=document_id)
        if not document_to_be_removed:
            return

        self.database.session.delete(document_to_be_removed)
        self.database.session.commit()
        self.log.debug("Entity deleted.")


NestedDocument = NamedTuple("NestedDocument", [("property_name", str),
                                               ("document_model", Model),
                                               ("differentiator_property", str)])


class WithNestedDocumentsStore(DefaultStore):
    """Generic datastore which can be used to work on entites from database, which contain nested entites.

    For example - a sqlalchemy.model with many-to-one relationship, encompasses other model in single list.
    This class makes it easy to persist changes not only to entity, but with those columns which interacts with it.
    """

    def __init__(self, model: T = None, database: SQLAlchemy = None, logger: Logger = None,
                 nested_documents_specs: List[NestedDocument] = None) -> None:
        """
        Initialize datastore instance.

        :param model: SQLAlchemy entity model which datastore will work upon (table).
        :param database: SQLAlchemy instance which should be used to connect to database.
        :param logger: Logger instance which should be used to log. Optional.
        :param nested_documents_specs: List[NestedDocuments]: list which specifies details about
        nested entities connected to given model. It should be a tuple, containing of key under which
        nested entity is attached to model, model representing nested entity and attribute name which should
        be used to differentiate between nested documents.
        """
        super().__init__(model=model, database=database, logger=logger)
        self.nested_documents_specs: List[NestedDocument] = nested_documents_specs
        self._load_nested_documents_properties_names()

    def _load_nested_documents_properties_names(self) -> None:
        """Load names of properties which are nested entities (and thus, should be ignored in default operations)."""
        for property_name, _, _ in self.nested_documents_specs:
            self.columns_to_ignore.append(property_name)

    @staticmethod
    def _persist_nested_document(entity: T = None, document: Dict = None,
                                 nested_doc_key: str = "", nested_doc_model: Model = None,
                                 differentiator_property: str = "") -> None:
        """
        Persist any changes made to nested properties of given sqlalchemy model.

        For example: if entity with tags (many-to-one relationship) will have tag removed, and than it will
        be stored via this class, this method will ensure the tag is removed.

        :param entity: entity upon which we are performing operations.
        :param document: dictionary which represents user request for given model.
        :param nested_doc_key: key under which nested entity is attached to model.
        :param nested_doc_model: model which represents nested entity.
        :param differentiator_property: attribute name which should  be used to differentiate between nested entities.
        """
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
        """Ensure any changes made to nested documents are persisted."""
        for nested_doc_key, nested_doc_model, differentiator_property in self.nested_documents_specs:
            self._persist_nested_document(entity=entity, document=document,
                                          nested_doc_key=nested_doc_key,
                                          nested_doc_model=nested_doc_model,
                                          differentiator_property=differentiator_property)
