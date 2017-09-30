def test_sanity() -> None:
    """Check if pytest is working."""
    from pipwatch_worker.main import main
    assert main is not None

    from pipwatch_worker.celery_components.application import app
    assert app is not None
