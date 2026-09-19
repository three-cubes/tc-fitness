from unittest.mock import Mock

import pytest

pytestmark = pytest.mark.integration


def test_status():
    client = Mock()
    assert client
