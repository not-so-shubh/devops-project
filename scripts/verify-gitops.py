"""Let Flux pull committed desired state and reconcile the existing Helm release."""

import json
import os
import subprocess
from pathlib import Path

sha = os.environ["GITHUB_SHA"]
objects = [
    {
        "apiVersion": "source.toolkit.fluxcd.io/v1",
        "kind": "GitRepository",
        "metadata": {"name": "stockpilot", "namespace": "flux-system"},
        "spec": {
            "interval": "1m",
            "url": "https://github.com/not-so-shubh/devops-project",
            "ref": {"branch": "main", "commit": sha},
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
    subprocess.run(command, check=True)
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
    "fetched_revision": revision,
    "deployment_environment": environment,
    "release_conditions": release["status"]["conditions"],
    "method": "Flux source-controller pulls committed gitops/ci; kustomize-controller substitutes tested SHA; helm-controller upgrades release and config checksum rolls Pods",
}
Path("docs/evidence/gitops-ci.json").write_text(json.dumps(proof, indent=2) + "\n")
print(
    "PASS: Flux pulled the exact Git revision and reconciled the Helm release; running Pod reflects committed GitOps configuration"
)
