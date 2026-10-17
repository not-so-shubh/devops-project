"""Prevent tracked historical evidence from being uploaded as a fresh run result."""

import os
from pathlib import Path

from evidence_files import EVIDENCE_FILES

if os.environ.get("GITHUB_ACTIONS") != "true":
    raise SystemExit("This cleanup is restricted to the disposable GitHub Actions checkout")
for name in EVIDENCE_FILES | {"ci-run.json"}:
    assert Path(name).name == name
    Path("docs/evidence", name).unlink(missing_ok=True)
print(
    "Cleared generated evidence from this disposable checkout; new artifacts must come from this run"
)
