from pathlib import Path


def test_toggle() -> None:
    marker = Path(__file__).with_name("already-ran")
    if marker.exists():
        raise AssertionError("second execution must expose the deterministic control")
    marker.touch()
