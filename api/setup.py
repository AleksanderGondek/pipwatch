from setuptools import setup, find_packages

from pipwatch_api.version import VERSION

setup(
    name="pipwatch_api",
    version=VERSION,
    packages=find_packages(),
)
