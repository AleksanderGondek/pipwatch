import os
from setuptools import setup, find_packages
from typing import List

from pipwatch_api.version import VERSION


def read_requirements() -> List[str]:
    """Read packages that are required by pipwatch api."""
    current_working_directory = os.path.abspath(os.path.dirname(__file__))
    requirements = []
    with open(os.path.join(current_working_directory, "requirements.txt"), encoding="utf-8") as file:
        requirements = [requirement.strip() for requirement in file.readlines()]

    return requirements


setup(
    name="pipwatch_api",
    version=VERSION,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=read_requirements(),
    include_package_data=True,
    license="Apache-2.0",
)
