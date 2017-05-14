import pytest

from pipwatch_api.datastore.models import Tag
from pipwatch_api.datastore.stores import DefaultStore


@pytest.fixture()
def default_store_fixture(database) -> DefaultStore:
    """To be described."""
    return DefaultStore(model=Tag, database=database)


class TestDefaultStore():
    """To be described."""
    def test_naive_get_columns_names(self, default_store_fixture) -> None:
        """To be described."""
        assert default_store_fixture._naive_get_columns_names() == ["name"]

    def test_create(self, default_store_fixture, mocker) -> None:
        """To be described."""
        mocker.spy(default_store_fixture, "_additional_document_handler")
        mocker.patch.object(default_store_fixture, "_naive_get_columns_names",
                            autospec=True, return_value=["name"])
        dictionary_representation_of_database_entity = {
            "name": "steffan muss",
            "other_property": "other_property_value"
        }

        entity_returned = default_store_fixture.create(document=dictionary_representation_of_database_entity)

        assert getattr(entity_returned, "name", None) == "steffan muss"
        assert getattr(entity_returned, "other_property", None) == None
        default_store_fixture._additional_document_handler.assert_called_once()
