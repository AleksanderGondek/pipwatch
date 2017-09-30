from setuptools import setup, find_packages

from pipwatch_api.version import VERSION

setup(
    name="pipwatch_api",
    version=VERSION,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "celery[redis]",
        "flask-restplus",
        "Flask-SQLAlchemy"
    ],
    include_package_data=False,
    license="Apache-2.0",
)
