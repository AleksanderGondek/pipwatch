"""This module contains various helper functions used throughout the worker."""
import os


def get_pip_script_name() -> str:
    """Return expected pip script name for os pipwatch is currently running on."""
    script_name = "pip"
    if os.name == "nt":
        script_name += ".exe"

    return script_name
