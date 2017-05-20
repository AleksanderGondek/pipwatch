"""This module contains fixtures that are used in resources tests."""
import pytest

from pipwatch_api.datastore.stores import DefaultStore, WithNestedDocumentsStore

@pytest.fixture()
def default_store_fixture(mocker) -> DefaultStore:
    """Test instance of default_store class."""
    instance = DefaultStore(model=None, database=None)
    mocker.patch.object(instance, "create", autospec=True)
    mocker.patch.object(instance, "read", autospec=True)
    mocker.patch.object(instance, "read_all", autospec=True)
    mocker.patch.object(instance, "update", autospec=True)
    mocker.patch.object(instance, "delete", autospec=True)
    return instance
