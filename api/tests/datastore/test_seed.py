"""This module contains unit tests for database seeding operations."""
from pipwatch_api.datastore.models import Namespace, Tag, Project, RequirementsFile, Requirement
from pipwatch_api.datastore.seed import seed_database


def test_seed_database(database) -> None:
    """Seed method should initialize database with exemplary data"""
    seed_database(database_instance=database)

    assert len(Namespace.query.all()) == 1
    assert len(Tag.query.all()) == 1
    assert len(Project.query.all()) == 1
    assert len(RequirementsFile.query.all()) == 2
    assert len(Requirement.query.all()) == 2
