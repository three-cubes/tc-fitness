#!/usr/bin/env bash
# Build release artifacts once, then prove both installed distribution paths.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
python_bin="python3"

usage() {
  echo "usage: $0 [--python PYTHON]" >&2
}

while (($#)); do
  case "$1" in
    --python)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      python_bin="$2"
      shift 2
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

workdir="$(mktemp -d "${TMPDIR:-/tmp}/tc-fitness-distribution.XXXXXX")"
trap 'rm -rf "$workdir"' EXIT
dist_dir="$workdir/dist"
rebuilt_dir="$workdir/rebuilt"
fixture_dir="$workdir/fixture"
runtime_requirements="$workdir/runtime-requirements.txt"
assurance_requirements="$workdir/assurance-requirements.txt"

mkdir -p "$dist_dir" "$rebuilt_dir" "$fixture_dir"
uv export --project "$repo_root" --locked --no-dev --no-emit-project \
  --format requirements.txt --output-file "$runtime_requirements" >/dev/null
uv export --project "$repo_root" --locked --no-dev --all-extras --no-emit-project \
  --format requirements.txt --output-file "$assurance_requirements" >/dev/null
uv build --python "$python_bin" --out-dir "$dist_dir" "$repo_root"

wheels=("$dist_dir"/*.whl)
sdists=("$dist_dir"/*.tar.gz)
[[ ${#wheels[@]} -eq 1 && -f "${wheels[0]}" ]] || { echo "expected one wheel" >&2; exit 1; }
[[ ${#sdists[@]} -eq 1 && -f "${sdists[0]}" ]] || { echo "expected one source distribution" >&2; exit 1; }

git init --quiet "$fixture_dir"
cat >"$fixture_dir/pyproject.toml" <<'EOF'
[tool.tc_fitness]
name = "distribution qualification fixture"

[[tool.tc_fitness.steps]]
id = "git-filesystem"
run = ["git", "rev-parse", "--is-inside-work-tree"]
EOF
cat >"$fixture_dir/runtime-contract.json" <<'EOF'
{"environments":{"qualification":{"targets":{"local":{"access":{},"deployment":{},"evidence":{},"filesystem":{}}}}},"schema":"tc-fitness/runtime-contract/v1"}
EOF

write_valid_evidence() {
  local python="$1"
  local resolved="$2"
  local evidence="$3"
  "$python" - "$resolved" "$evidence" <<'PY'
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

resolved = Path(sys.argv[1]).read_bytes()
evidence = {
    "schema": "tc-fitness/runtime-evidence/v1",
    "contract_digest": "sha256:" + hashlib.sha256(resolved).hexdigest(),
    "source_sha": "a" * 40,
    "image_digest": "sha256:" + "b" * 64,
    "host_id": "distribution-qualification",
    "runtime_user": "qualification",
    "deployment_id": "distribution-qualification",
    "configuration_identity": "sha256:" + "c" * 64,
    "run_id": 1,
    "attempt_id": 1,
    "captured_at": datetime.now(UTC).isoformat(),
    "checks": [
        {
            "id": "distribution-fixture",
            "status": "passed",
            "observation": {"kind": "process", "state": "healthy"},
        }
    ],
    "artifacts": [],
}
Path(sys.argv[2]).write_bytes(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode() + b"\n")
PY
}

qualify() {
  local label="$1"
  local wheel="$2"
  local environment="$workdir/$label-env"
  local resolved="$workdir/$label-resolved.json"
  local evidence="$workdir/$label-evidence.json"
  local verification="$workdir/$label-verification.json"

  uv venv --clear --no-project --python "$python_bin" "$environment"
  # The installed candidate remains an index-free artifact install. Its required
  # runtime dependency is resolved from this repository's locked environment
  # before that proof, rather than treating the post-Task-2 package as stdlib-only.
  uv pip install --python "$environment/bin/python" --require-hashes -r "$runtime_requirements"
  uv pip install --no-deps --no-index --python "$environment/bin/python" "$wheel"

  "$environment/bin/python" -c 'import coverage'
  "$environment/bin/tc-fitness" --help >/dev/null
  "$environment/bin/tc-fitness" assure-coverage --help >/dev/null
  "$environment/bin/tc-fitness" run --repo-root "$fixture_dir"
  "$environment/bin/tc-fitness-runtime-contract" --help >/dev/null
  "$environment/bin/tc-fitness-runtime-contract" resolve \
    --contract "$fixture_dir/runtime-contract.json" \
    --environment qualification \
    --target local \
    --output "$resolved"
  write_valid_evidence "$environment/bin/python" "$resolved" "$evidence"
  "$environment/bin/tc-fitness-runtime-contract" verify-evidence \
    --contract "$fixture_dir/runtime-contract.json" \
    --environment qualification \
    --target local \
    --evidence "$evidence" \
    --expected-source-sha "$(printf 'a%.0s' {1..40})" \
    --expected-image-digest "sha256:$(printf 'b%.0s' {1..64})" \
    --expected-host-id distribution-qualification \
    --expected-runtime-user qualification \
    --expected-deployment-id distribution-qualification \
    --expected-configuration-identity "sha256:$(printf 'c%.0s' {1..64})" \
    --expected-run-id 1 \
    --expected-attempt-id 1 \
    --required-check distribution-fixture \
    --max-age-seconds 300 \
    --output "$verification"

  # Coverage parsing is an assurance extra, not a default-install dependency.
  uv pip install --python "$environment/bin/python" --require-hashes -r "$assurance_requirements"
  "$environment/bin/python" - "$workdir/$label-coverage" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
root.mkdir()
(root / "src/tc_fitness").mkdir(parents=True)
(root / "tests").mkdir()
(root / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n")
(root / "pyproject.toml").write_text(
    "[project]\nname='installed-assurance-fixture'\nversion='0.0.0'\nrequires-python='>=3.12'\n"
    "[project.optional-dependencies]\ndev=['coverage==7.14.2','pytest==9.1.0']\n"
)

def run(*args):
    return subprocess.run(args, cwd=root, check=True, capture_output=True, text=True, timeout=90).stdout.strip()

def commit():
    run("git", "add", ".")
    run("git", "-c", "user.name=Contract", "-c", "user.email=contract@example.invalid", "commit", "-qm", "fixture")
    return run("git", "rev-parse", "HEAD")

run("git", "init", "-q")
run("uv", "lock", "--python", sys.executable)
source = root / "src/tc_fitness/subject.py"
source.write_text("def choose(flag):\n    return 1\n")
test = root / "tests/test_subject.py"
test.write_text(
    "import runpy\nimport pytest\npytestmark=pytest.mark.integration\n"
    "def test_choices():\n    choose=runpy.run_path('src/tc_fitness/subject.py')['choose']\n"
    "    assert choose(False)==1\n"
)
# Fixed critical predicates must be present even in the tiny shipped-surface proof.
for name in ("gate", "runner", "gate_config", "runtime_contract"):
    (root / f"src/tc_fitness/{name}.py").write_text("")
base = commit()
source.write_text("def choose(flag):\n    if flag:\n        return 2\n    return 1\n")
test.write_text(test.read_text() + "    assert choose(True)==2\n")
candidate = commit()
payload = json.loads(run(
    str(Path(sys.executable).with_name("tc-fitness")), "assure-coverage", "--repo-root", str(root),
    "--base-commit", base, "--candidate-commit", candidate,
))
if (payload["status"] != "pass" or payload["base"]["commit"] != base
        or payload["candidate"]["commit"] != candidate
        or payload["base"]["counts"]["branches"] != 0
        or payload["candidate"]["counts"]["covered_branches"] != 2):
    raise SystemExit("installed coverage transaction did not prove the exact A/B branch change")
PY
  echo "qualified $label coverage transaction"
}

cd "$workdir"
qualify "direct-wheel" "${wheels[0]}"
echo "qualified direct wheel"

# uv's default PEP 517 build uses isolated build dependencies; do not add
# --no-build-isolation here.
uv build --python "$python_bin" --wheel --out-dir "$rebuilt_dir" "${sdists[0]}"
rebuilt_wheels=("$rebuilt_dir"/*.whl)
[[ ${#rebuilt_wheels[@]} -eq 1 && -f "${rebuilt_wheels[0]}" ]] || {
  echo "expected one wheel rebuilt from source distribution" >&2
  exit 1
}
qualify "wheel-from-sdist" "${rebuilt_wheels[0]}"
echo "qualified wheel rebuilt from sdist"
