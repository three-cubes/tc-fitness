import pytest

pytestmark = pytest.mark.integration


def test_status(tmp_path):
    output = tmp_path / "result"
    output.write_text("ready")
    assert output.read_text() == "ready"
