"""This module contains fixtures that are used in resources tests."""
from typing import Any, Dict, Optional

import pytest

from pipwatch_api.datastore.stores import DefaultStore

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


def get_model_repr(**kwargs) -> Optional[Dict[str, Any]]:
    """Return dictionary-like representation of given model."""
    model: Dict[str, Any] = kwargs.get("model")
    if not model:
        return None

    model_representation = {
        key: None for key in model.keys()
    }

    kwargs.pop("model")
    for key, value in kwargs.items():
        model_representation[key] = value

    return model_representation
