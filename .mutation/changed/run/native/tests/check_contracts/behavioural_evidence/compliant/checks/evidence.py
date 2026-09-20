import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "src" / "producer.py"


def test_producer(tmp_path):
    output = tmp_path / "result.txt"
    result = subprocess.run([str(PRODUCER), str(output)], capture_output=True, check=False)
    assert result.returncode == 0
    assert output.read_text() == "produced\n"
