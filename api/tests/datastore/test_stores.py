import pytest

from pipwatch_api.datastore.stores import DefaultStore


class ModelMock():
    id = 0
    name = ""
    __table__ = object()

    def __init__(self, name: str = "") -> None:
        self.name = name


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
