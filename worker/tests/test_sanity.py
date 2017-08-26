def test_sanity() -> None:
    """Check if pytest is working."""
    from pipwatch_worker.main import main
    assert main is not None
