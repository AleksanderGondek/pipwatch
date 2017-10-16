"""This module contains handler functions that should be run before each application request."""
from logging import getLogger, Logger

from flask import request


log: Logger = getLogger(__name__)


def log_incoming_request() -> None:
    """Fully log incoming request for debbuging purposes."""
    # This is possible security vulnerability, please see: http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
    x_forwarded_for = next(iter(request.headers.getlist("X-Forwarded-For")), None)
    request_origin = x_forwarded_for if x_forwarded_for else request.remote_addr
    log.debug("Received %s request for path '%s' from %s", request.method, request.path, request_origin)
