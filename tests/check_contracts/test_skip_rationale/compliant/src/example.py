import pytest


@pytest.mark.skipif(False, reason="Only skip when the platform lacks this feature")
def test_sample():
    assert 2 + 3 == 5
