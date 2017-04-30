"""This module contains logic for creating pipwatch api app instance."""

from flask import Flask

from pipwatch_api.core.configuration import configure_flask_application, configure_sqlalchemy
from pipwatch_api.datastore.models import DATABASE
from pipwatch_api.namespaces.version_one import get_api_version_one


def get_flask_application() -> Flask:
    """Return configured restplus api application."""
    app = Flask(__name__)

    configure_flask_application(application=app)
    configure_sqlalchemy(application=app, sql_alchemy_instance=DATABASE)

    app.register_blueprint(blueprint=get_api_version_one())

    return app
