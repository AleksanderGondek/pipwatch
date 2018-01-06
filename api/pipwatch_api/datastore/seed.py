"""This modules contains logic responsible for seeding the database with default values."""
from flask_sqlalchemy import SQLAlchemy

from pipwatch_api.datastore.models import GitRepository, Namespace, Tag, Project, RequirementsFile, Requirement


def seed_database(database_instance: SQLAlchemy = None) -> None:
    """Seed the passed-in database instance with default data."""
    default_namespace = Namespace(name="default")
    example_tag = Tag(name="example")
    example_git_repository = GitRepository(
        flavour="git",
        url="git@github.com:AleksanderGondek/pipwatch.git",
    )
    default_project = Project(
        name="pipwatch_api",
        check_command="tox"
    )
    example_requirements_file = RequirementsFile(path="api/requirements.txt", status="")
    example_dev_requirements_file = RequirementsFile(path="api/requirements-development.txt", status="")

    example_requirement = Requirement(name="SQLAlchemy", current_version="1.1.14", desired_version="", status="")
    example_dev_requirement = Requirement(name="pytest", current_version="3.2.2", desired_version="", status="")

    database_instance.session.add(default_namespace)
    database_instance.session.add(example_tag)
    database_instance.session.add(example_git_repository)
    database_instance.session.add(default_project)
    database_instance.session.add(example_requirements_file)
    database_instance.session.add(example_dev_requirements_file)
    database_instance.session.add(example_requirement)
    database_instance.session.add(example_dev_requirement)
    database_instance.session.commit()

    example_git_repository.project_id = default_project.id
    default_namespace.projects.append(default_project)
    example_requirements_file.requirements.append(example_requirement)
    example_dev_requirements_file.requirements.append(example_dev_requirement)
    database_instance.session.commit()

    default_project.tags.append(example_tag)
    default_project.requirements_files.append(example_requirements_file)
    default_project.requirements_files.append(example_dev_requirements_file)
    database_instance.session.commit()
