"""Exercise two isolated defects and prove repairs without changing working Services."""

import json
import os
import subprocess
import time
from pathlib import Path


def kubectl(*args):
    return subprocess.check_output(["kubectl", "-n", "stockpilot", *args], text=True)


def endpoints():
    data = json.loads(
        kubectl(
            "get",
            "endpointslice",
            "-l",
            "kubernetes.io/service-name=stockpilot-lab-empty-service",
            "-o",
            "json",
        )
    )
    return [
        address
        for item in data["items"]
        for endpoint in (item.get("endpoints") or [])
        for address in endpoint["addresses"]
    ]


observations = []
try:
    kubectl("apply", "-f", "troubleshooting/broken-service.yaml")
    time.sleep(3)
    assert not endpoints(), "The intentionally incorrect selector unexpectedly matched Pods"
    observations.append(
        {"issue": "empty Service", "root_cause": "selector matches no Pod", "before_addresses": 0}
    )
    patch = {
        "spec": {
            "selector": {
                "app.kubernetes.io/component": "backend",
                "app.kubernetes.io/instance": "stockpilot",
            }
        }
    }
    kubectl("patch", "svc", "stockpilot-lab-empty-service", "--type=merge", "-p", json.dumps(patch))
    for _ in range(15):
        if endpoints():
            break
        time.sleep(2)
    assert len(endpoints()) >= 2
    observations[-1]["after_addresses"] = len(endpoints())
    observations[-1]["verification"] = "At least two backend endpoints restored"

    kubectl("apply", "-f", "troubleshooting/broken-image.yaml")
    reason = ""
    for _ in range(45):
        pods = json.loads(kubectl("get", "pods", "-l", "app=stockpilot-lab", "-o", "json"))
        for pod in pods["items"]:
            for container in pod["status"].get("containerStatuses", []):
                reason = container.get("state", {}).get("waiting", {}).get("reason", "")
        if reason in {"ErrImagePull", "ImagePullBackOff"}:
            break
        time.sleep(2)
    assert reason in {"ErrImagePull", "ImagePullBackOff"}, reason
    observations.append(
        {"issue": "bad image tag", "root_cause": "nonexistent image tag", "observed_reason": reason}
    )
    image = f"ghcr.io/not-so-shubh/stockpilot-backend:{os.environ['GITHUB_SHA']}"
    kubectl("set", "image", "deployment/stockpilot-lab-bad-image", f"lab={image}")
    kubectl("rollout", "status", "deployment/stockpilot-lab-bad-image", "--timeout=120s")
    response = kubectl(
        "exec",
        "deployment/stockpilot-lab-bad-image",
        "--",
        "python",
        "-c",
        "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())",
    )
    assert json.loads(response)["status"] == "UP"
    observations[-1]["verification"] = "Correct scanned SHA image starts and /health responds UP"
    Path("docs/evidence/troubleshooting-ci.json").write_text(
        json.dumps(observations, indent=2) + "\n"
    )
    print("PASS: observed, diagnosed, repaired and verified isolated Service and image failures")
finally:
    kubectl(
        "delete",
        "-f",
        "troubleshooting/broken-service.yaml",
        "-f",
        "troubleshooting/broken-image.yaml",
        "--ignore-not-found",
    )
