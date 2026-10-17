"""Copy only an explicit allowlist of synthetic CI evidence into the repository."""

import importlib.util
import json
import os
from pathlib import Path

names = set(
    [
        "pytest-postgres.txt",
        "bandit.json",
        "secrets.json",
        "terraform-ci-validate.txt",
        "terraform-ci-mock-test.txt",
        "compose-ci.txt",
        "compose-ci.log",
        "compose-smoke.txt",
        "metrics.txt",
        "frontend-desktop.png",
        "frontend-mobile.png",
        "create-dialog-desktop.png",
        "create-dialog-mobile.png",
        "kubernetes-ci.txt",
        "troubleshooting-ci.json",
        "gitops-ci.json",
        "helm-release-ci.txt",
        "hpa-metrics-ci.txt",
        "cluster-pods-ci.txt",
        "cluster-events-ci.txt",
        "migration-ci.log",
        "prometheus-targets.json",
        "prometheus-query.json",
        "grafana-dashboard.png",
        "prometheus-targets.png",
        "trivy-backend.json",
        "trivy-frontend.json",
    ]
)
spec = importlib.util.spec_from_file_location("evidence_redactor", "scripts/redact-evidence.py")
redactor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(redactor)
destination = Path("docs/evidence")
destination.mkdir(parents=True, exist_ok=True)
written = []
for source in Path(os.environ["EVIDENCE_DOWNLOAD_DIR"]).rglob("*"):
    if source.is_file() and source.name in names:
        if source.suffix == ".png":
            (destination / source.name).write_bytes(source.read_bytes())
        elif source.suffix == ".json":
            data = redactor.redact_json(json.loads(source.read_text()))
            (destination / source.name).write_text(json.dumps(data, indent=2) + "\n")
        else:
            (destination / source.name).write_text(redactor.redact(source.read_text()))
        written.append(source.name)
metadata = {
    "source_sha": os.environ["GITHUB_SHA"],
    "run_id": os.environ["GITHUB_RUN_ID"],
    "run_url": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
    "files": sorted(set(written)),
    "scope": "Actual CI evidence; consult job results for success/failure. AWS apply/destroy not performed.",
    "job_results": json.loads(os.environ.get("VERIFICATION_RESULTS", "{}")),
}
(destination / "ci-run.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(
    f"Archived {len(set(written))} allowed evidence files; no credentials or raw browser traces copied."
)
