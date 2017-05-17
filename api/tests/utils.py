"""This module contains various helpers used in testing."""
import json

from flask import Response
from werkzeug.utils import cached_property


class JSONResponse(Response):
    """Wrapper around default flask response, allowing for easier accessing response content."""

    @cached_property
    def json(self):
        return json.loads(self.get_data(as_text=True))
