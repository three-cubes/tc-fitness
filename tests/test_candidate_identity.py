"""Executing package identity is stable across native worker result writes."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import tc_fitness
from tc_fitness.check_contract_execution import tree_digest

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("native_results", [False, True])
def test_only_paired_native_result_files_are_execution_metadata(tmp_path: Path, native_results: bool) -> None:
    source = tmp_path / "policy.py"
    source.write_text("REQUIRED = True\n")
    result = tmp_path / "policy.py.meta"
    result.write_text('{"result": 0}')
    before = tree_digest(tmp_path, ignore_native_results=native_results)
    result.write_text('{"result": 1}')
    after = tree_digest(tmp_path, ignore_native_results=native_results)
    assert (after == before) is native_results
    source.write_text("REQUIRED = False\n")
    assert tree_digest(tmp_path, ignore_native_results=native_results) != after
    before = tree_digest(tmp_path, ignore_native_results=native_results)
    (tmp_path / "unpaired.py.meta").write_text("resource")
    assert tree_digest(tmp_path, ignore_native_results=native_results) != before
    before = tree_digest(tmp_path, ignore_native_results=native_results)
    (tmp_path / "directory.py").write_text("VALUE = 1\n")
    (tmp_path / "directory.py.meta").mkdir()
    assert tree_digest(tmp_path, ignore_native_results=native_results) != before


def test_concurrent_native_results_do_not_change_bound_candidate_inputs(tmp_path: Path) -> None:
    package = tmp_path / "tc_fitness"
    shutil.copytree(Path(tc_fitness.__file__).parent, package)
    script = r"""
import json
from pathlib import Path
from threading import Event, Thread
from tc_fitness.check_contract_execution import candidate_identity, tree_digest

package = Path("tc_fitness")
metadata = package / "coverage_admission.py.meta"
metadata.write_text('{"result": 0}')
expected = candidate_identity()
all_inputs = tree_digest(package, ignore_caches=True)
stop = Event()
started = Event()

def worker():
    index = 0
    while not stop.is_set():
        metadata.write_text(json.dumps({"result": index}))
        started.set()
        index += 1

thread = Thread(target=worker)
thread.start()
started.wait()
try:
    observed = [candidate_identity() for _ in range(25)]
finally:
    stop.set()
    thread.join()
assert all(value == expected for value in observed), "mutable native results changed engine identity"
metadata.write_text('{"result": "terminal"}')
assert tree_digest(package, ignore_caches=True) != all_inputs
assert candidate_identity() == expected
source = package / "coverage_admission.py"
source.write_bytes(source.read_bytes() + b"\n# changed production input\n")
changed_source = candidate_identity()
assert changed_source != expected
resource = package / "policy.json"
resource.write_text('{"required": true}')
changed_resource = candidate_identity()
assert changed_resource != changed_source
resource.write_text('{"required": false}')
assert candidate_identity() != changed_resource
expected = candidate_identity()
(package / "unpaired.py.meta").write_text("candidate resource, not a native source sidecar")
assert candidate_identity() != expected
print(json.dumps({"stable_observations": len(observed), "source_and_policy_bound": True}))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(tmp_path)},
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"stable_observations": 25, "source_and_policy_bound": True}
