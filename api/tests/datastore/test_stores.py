from sqlalchemy.orm.exc import NoResultFound
import pytest

from pipwatch_api.datastore.stores import DefaultStore


class ModelMock():
    id = 0
    name = ""
    query = object()
    __table__ = object()

    def __init__(self, name: str = "", id: int = 0) -> None:
        self.name = name
        if id > 0:
            self.id = id


@pytest.fixture()
def default_store_fixture(database) -> DefaultStore:
    """To be described."""
    return DefaultStore(model=ModelMock, database=database)


class TestDefaultStore():
    """Test behaviour of DefaultStore class."""
    def test_naive_get_columns_names(self, default_store_fixture, mocker) -> None:
        """Should return all column names for given entity, except for blacklisted ones."""
        mocker.patch.object(ModelMock, "__table__")
        ModelMock.__table__.columns.keys.return_value = ["id", "name"]
        assert default_store_fixture._naive_get_columns_names() == ["name"]

    def test_create(self, default_store_fixture, mocker) -> None:
        """Should create a valid instance of entity, based on passed in dictionary."""
        mocker.spy(default_store_fixture, "_additional_document_handler")
        mocker.patch.object(default_store_fixture.database.session, "add", autospec=True)
        mocker.patch.object(default_store_fixture, "_naive_get_columns_names",
                            autospec=True, return_value=["name"])
        dictionary_representation_of_database_entity = {
            "name": "steffan muss",
            "other_property": "other_property_value"
        }

        entity_returned = default_store_fixture.create(document=dictionary_representation_of_database_entity)

        assert getattr(entity_returned, "name", None) == "steffan muss"
        assert getattr(entity_returned, "other_property", None) == None
        default_store_fixture.database.session.add.assert_called_once()
        default_store_fixture._additional_document_handler.assert_called_once()

    def test_read(self, default_store_fixture, mocker) -> None:
        """Should retrieve document with passes in id from database."""
        mocked_response = object()
        mocker.patch.object(default_store_fixture.model, "query")
        default_store_fixture.model.query.filter.return_value.one.return_value = mocked_response

        assert default_store_fixture.read(document_id=4) == mocked_response

    def test_read_document_not_found(self, default_store_fixture, mocker) -> None:
        """Should return None if document with passed in id has not been found."""
        mocker.patch.object(default_store_fixture.model, "query")
        default_store_fixture.model.query.filter.return_value.one.side_effect = NoResultFound()

        assert default_store_fixture.read(document_id=4) is None

    def test_read_all(self, default_store_fixture, mocker) -> None:
        """Should return all entities from database."""
        mocked_response = object()
        mocker.patch.object(default_store_fixture.model, "query")
        default_store_fixture.model.query.all.return_value = [mocked_response]

        assert default_store_fixture.read_all() == [mocked_response]

    def test_update_document_not_found(self, default_store_fixture, mocker) -> None:
        """Should return 'None' if document with given id is not found."""
        mocker.patch.object(default_store_fixture, "read", return_value=None)
        assert default_store_fixture.update(document_id=-32, document={}) is None

    def test_update_document(self, default_store_fixture, mocker) -> None:
        """Should load document with given id and update all fields passed in."""
        existing_document = ModelMock(name="should_change", id=2)
        mocker.patch.object(default_store_fixture, "read", return_value=existing_document)
        mocker.spy(default_store_fixture, "_additional_document_handler")
        mocker.patch.object(default_store_fixture.database.session, "add", autospec=True)
        mocker.patch.object(default_store_fixture, "_naive_get_columns_names",
                            autospec=True, return_value=["name"])
        update_dictionary_repr = {
            "id": "maliciously_injected_id",
            "name": "changed",
            "to_be_ignored": "to_be_ignored"
        }

        returned_document = default_store_fixture.update(document_id=-32, document=update_dictionary_repr)
        assert returned_document.name == "changed"
        assert returned_document.id == 2
        default_store_fixture.database.session.add.assert_called_once()
        default_store_fixture._additional_document_handler.assert_called_once()

    def test_delete_document_not_found(self, default_store_fixture, mocker) -> None:
        """Should not do anything if passed in document id is not found."""
        mocker.patch.object(default_store_fixture, "read", return_value=None)
        mocker.patch.object(default_store_fixture.database.session, "delete", autospec=True)
        default_store_fixture.delete(document_id=-32)
        assert default_store_fixture.database.session.delete.call_count == 0

    def test_delete_document(self, default_store_fixture, mocker) -> None:
        """Should remove document with id which was passed in."""
        returned_object = object()
        mocker.patch.object(default_store_fixture, "read", return_value=returned_object)
        mocker.patch.object(default_store_fixture.database.session, "delete", autospec=True)
        default_store_fixture.delete(document_id=-32)
        default_store_fixture.database.session.delete.assert_called_with(returned_object)
