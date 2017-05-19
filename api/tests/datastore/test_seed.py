"""This module contains unit tests for database seeding operations."""
from pipwatch_api.datastore.models import Namespace, Tag, Project, RequirementsFile, Requirement
from pipwatch_api.datastore.seed import seed_database


def test_seed_database(database) -> None:
    """Seed method should initialize database with exemplary data."""
    expected_namespace_name = "default"
    expected_tag_name = "example"

    expected_project_name = "pipwatch_api"
    expected_project_url = "https://github.com/AleksanderGondek/pipwatch/api"

    expected_requirements_files_paths = ["api/requirements.txt", "api/requirements-development.txt"]
    expected_requirements_names = ["requests", "pytest"]

    seed_database(database_instance=database)

    namespace_found = Namespace.query.first()
    assert namespace_found is not None and namespace_found.name == expected_namespace_name

    tag_found = Tag.query.first()
    assert tag_found is not None and tag_found.name == expected_tag_name

    project_found = Project.query.first()
    assert (project_found is not None
            and project_found.name == expected_project_name
            and project_found.url == expected_project_url)


    requirements_files_found = RequirementsFile.query.limit(2).all()
    assert requirements_files_found is not None and len(requirements_files_found) == 2
    for requirements_file in requirements_files_found:
        assert requirements_file.full_path in expected_requirements_files_paths

    requirements_found = Requirement.query.limit(2).all()
    assert requirements_found is not None and len(requirements_found) == 2
    for requirement_found in requirements_found:
        assert requirement_found.name in expected_requirements_names
