"""This module contains handler functions that should be run after each application request."""
from flask import request


def allow_any_cors_request(response: request) -> None:
    """While running in development mode allow requests from any domain."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
