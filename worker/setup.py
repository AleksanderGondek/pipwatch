from setuptools import setup, find_packages

from pipwatch_worker.version import VERSION

setup(
    name="pipwatch_worker",
    version=VERSION,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "flask-restplus",
        "Flask-SQLAlchemy"
    ],
    include_package_data=False,
    license="Apache-2.0",
)
