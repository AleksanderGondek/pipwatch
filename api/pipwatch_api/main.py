"""This module contains logic responsible starting the pipwatch api."""

from logging import getLogger, Logger

from flask import Flask
from flask_restplus import Resource, Api

from pipwatch_api.configuration import configure_flask_application, configure_logger

app = Flask(__name__)
api = Api(app)


@api.route("/hello")
class HelloWorld(Resource):
    """Api resource test."""
    def get(self):  # pylint: disable=no-self-use
        """Return hello world."""
        return {"hello": "world"}


if __name__ == "__main__":
    configure_logger()
    log: Logger = getLogger(__name__)

    log.debug("Attempting to configure flask application..")
    configure_flask_application(application=app)
    log.debug("Flask application configured")
    app.run()
