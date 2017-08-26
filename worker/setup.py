from setuptools import setup, find_packages

from pipwatch_worker.version import VERSION

setup(
    name="pipwatch_worker",
    version=VERSION,
    packages=find_packages(),
)
