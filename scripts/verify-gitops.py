"""Let Flux pull committed desired state and reconcile the existing Helm release."""

import json
import os
import subprocess
from pathlib import Path

sha = os.environ.get("SOURCE_SHA") or os.environ["GITHUB_SHA"]
# Use a commit reachable from a real source branch. All PR jobs check out and
# tag this same head SHA; main pushes use the actual main commit.
source_branch = os.environ.get("SOURCE_BRANCH", "main")
source_repository = os.environ.get("SOURCE_REPOSITORY", "not-so-shubh/devops-project")
objects = [
    {
        "apiVersion": "source.toolkit.fluxcd.io/v1",
        "kind": "GitRepository",
        "metadata": {"name": "stockpilot", "namespace": "flux-system"},
        "spec": {
            "interval": "1m",
            "url": f"https://github.com/{source_repository}",
            "ref": {"branch": source_branch, "commit": sha},
        },
    },
    {
        "apiVersion": "kustomize.toolkit.fluxcd.io/v1",
        "kind": "Kustomization",
        "metadata": {"name": "stockpilot-ci", "namespace": "flux-system"},
        "spec": {
            "interval": "1m",
            "path": "./gitops/ci",
            "prune": True,
            "sourceRef": {"kind": "GitRepository", "name": "stockpilot"},
            "postBuild": {"substitute": {"IMAGE_SHA": sha}},
            "wait": True,
            "timeout": "7m",
        },
    },
]
for obj in objects:
    subprocess.run(["kubectl", "apply", "-f", "-"], input=json.dumps(obj), text=True, check=True)
for command in [
    [
        "kubectl",
        "wait",
        "-n",
        "flux-system",
        "--for=condition=Ready",
        "gitrepository/stockpilot",
        "--timeout=180s",
    ],
    [
        "kubectl",
        "wait",
        "-n",
        "flux-system",
        "--for=condition=Ready",
        "kustomization/stockpilot-ci",
        "--timeout=480s",
    ],
    [
        "kubectl",
        "wait",
        "-n",
        "stockpilot",
        "--for=condition=Ready",
        "helmrelease/stockpilot",
        "--timeout=180s",
    ],
    [
        "kubectl",
        "rollout",
        "status",
        "-n",
        "stockpilot",
        "deployment/stockpilot-backend",
        "--timeout=180s",
    ],
]:
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        # Preserve the actual source/reconciliation cause before CI deletes kind.
        with Path("docs/evidence/gitops-diagnostics-ci.txt").open("w") as stream:
            for namespace, resource in [
                ("flux-system", "gitrepository/stockpilot"),
                ("flux-system", "kustomization/stockpilot-ci"),
                ("stockpilot", "helmrelease/stockpilot"),
            ]:
                subprocess.run(
                    ["kubectl", "describe", "-n", namespace, resource],
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
        raise
environment = subprocess.check_output(
    [
        "kubectl",
        "exec",
        "-n",
        "stockpilot",
        "deployment/stockpilot-backend",
        "--",
        "printenv",
        "APP_ENV",
    ],
    text=True,
).strip()
assert environment == "gitops-ci", environment
source = json.loads(
    subprocess.check_output(
        ["kubectl", "get", "gitrepository/stockpilot", "-n", "flux-system", "-o", "json"], text=True
    )
)
release = json.loads(
    subprocess.check_output(
        ["kubectl", "get", "helmrelease/stockpilot", "-n", "stockpilot", "-o", "json"], text=True
    )
)
revision = source["status"]["artifact"]["revision"]
assert sha in revision
assert release["spec"]["values"]["backend"]["tag"] == sha
proof = {
    "source_sha": sha,
    "source_branch": source_branch,
    "source_repository": source_repository,
    "fetched_revision": revision,
    "deployment_environment": environment,
    "release_conditions": release["status"]["conditions"],
    "method": "Flux source-controller pulls committed gitops/ci; kustomize-controller substitutes tested SHA; helm-controller upgrades release and config checksum rolls Pods",
}
Path("docs/evidence/gitops-ci.json").write_text(json.dumps(proof, indent=2) + "\n")
print(
    "PASS: Flux pulled the exact Git revision and reconciled the Helm release; running Pod reflects committed GitOps configuration"
)
