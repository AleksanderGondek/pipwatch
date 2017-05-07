"""This module contains logic for creating pipwatch api app instance."""
from typing import Dict

from flask import Flask

from pipwatch_api.core.configuration import configure_flask_application, configure_sqlalchemy
from pipwatch_api.datastore.models import DATABASE
from pipwatch_api.namespaces.version_one import get_api_version_one


def get_flask_application(settings_override: Dict = None) -> Flask:
    """Return configured restplus api application."""
    app = Flask(__name__)

    configure_flask_application(application=app, settings_override=settings_override)
    if not settings_override:
        # Run only if not under tests
        configure_sqlalchemy(application=app, sql_alchemy_instance=DATABASE)

    app.register_blueprint(blueprint=get_api_version_one())

    return app
