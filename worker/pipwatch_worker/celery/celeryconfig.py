"""This is default celery configuration file."""

broker_url = "redis://localhost:6379/0"  # pylint: disable=invalid-name
imports = ["pipwatch_worker.celery.tasks"]  # pylint: disable=invalid-name
result_backend = "redis://localhost:6379/0"  # pylint: disable=invalid-name
