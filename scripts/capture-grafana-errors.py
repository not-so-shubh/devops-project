"""Retain actual Grafana error lines after redacting known CI credentials and metadata."""

import base64
import importlib.util
import json
import re
import subprocess
from pathlib import Path


def read(*args):
    result = subprocess.run(["kubectl", *args], text=True, capture_output=True, check=False)
    return result.stdout if result.returncode == 0 else ""


sensitive = []
for namespace, name in [("monitoring", "stockpilot-grafana"), ("stockpilot", "stockpilot-db")]:
    raw = read("get", "secret", name, "-n", namespace, "-o", "json")
    if raw:
        for key, encoded in json.loads(raw).get("data", {}).items():
            if re.search(r"password|token|url|auth", key, re.I):
                sensitive.extend([encoded, base64.b64decode(encoded).decode()])
logs = read(
    "logs",
    "-n",
    "monitoring",
    "deployment/monitoring-grafana",
    "-c",
    "grafana",
    "--previous",
    "--tail=200",
)
if not logs:
    logs = read(
        "logs", "-n", "monitoring", "deployment/monitoring-grafana", "-c", "grafana", "--tail=200"
    )
for value in sensitive:
    logs = logs.replace(value, "<REDACTED_CREDENTIAL>")
spec = importlib.util.spec_from_file_location("redactor", "scripts/redact-evidence.py")
redactor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(redactor)
lines = [
    redactor.redact(line)
    for line in logs.splitlines()
    if re.search(r"error|fatal|panic|failed|oom", line, re.I)
]
result = (
    "Actual Grafana error excerpt; known credential values and environment identifiers redacted.\n"
    + "\n".join(
        lines or ["No matching Grafana error lines available; inspect container state diagnostics."]
    )
    + "\n"
)
Path("docs/evidence/grafana-errors-ci.log").write_text(result)
print(result)
