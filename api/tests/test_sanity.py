def test_sanity() -> None:
    """Check if pytest is working."""
    from pipwatch_api.main import main
    assert main is not None
