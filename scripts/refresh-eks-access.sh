#!/usr/bin/env bash
# Restore the existing CloudShell operator /32 without changing other EKS settings.
set -euo pipefail
umask 077
export AWS_REGION=ap-southeast-2 AWS_DEFAULT_REGION=ap-southeast-2 AWS_PAGER=""
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
python3 - <<'PY'
import ipaddress
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

def eks(*args):
    return json.loads(subprocess.check_output(
        ["aws", "eks", *args, "--region", "ap-southeast-2",
         "--output", "json"], text=True))

path = Path("terraform/cloudshell.auto.tfvars.json")
values = json.loads(path.read_text())
assert values["aws_region"] == "ap-southeast-2", "Unexpected Terraform region"
with urllib.request.urlopen("https://checkip.amazonaws.com", timeout=15) as response:
    address = ipaddress.ip_address(response.read().decode().strip())
assert address.version == 4 and address.is_global, "Unexpected source IP"
desired = [f"{address}/32"]

cluster = eks("describe-cluster", "--name", "stockpilot-eks")["cluster"]
assert cluster["status"] == "ACTIVE", "Cluster update in progress; retry when ACTIVE"
assert cluster["arn"].split(":")[4] == values["admin_principal_arn"].split(":")[4], "Account mismatch"
config = cluster["resourcesVpcConfig"]
assert config["endpointPrivateAccess"] and config["endpointPublicAccess"], "Unexpected endpoint settings"
current = config["publicAccessCidrs"]
assert len(current) == 1 and ipaddress.ip_network(current[0]).prefixlen == 32, "Unexpected access list; stopped"
assert values["admin_cidrs"] in (current, desired), "Unexpected Terraform access settings"

if values["admin_cidrs"] != desired:
    backup = Path.home() / "stockpilot-private-backups"
    backup.mkdir(mode=0o700, exist_ok=True)
    (backup / f"before-ip-refresh-{time.time_ns()}.json").write_text(path.read_text())
    values["admin_cidrs"] = desired
    pending = path.with_name(path.name + ".pending.tfvars.json")
    pending.write_text(json.dumps(values, indent=2) + "\n")
    pending.chmod(0o600)
    os.replace(pending, path)
    print("Private Terraform variables synchronized.")

if current != desired:
    print("CloudShell IP changed. Updating the operator /32 only.", flush=True)
    update = eks("update-cluster-config", "--name", "stockpilot-eks",
                 "--resources-vpc-config",
                 json.dumps({"publicAccessCidrs": desired}))["update"]
    for attempt in range(60):
        status = eks("describe-update", "--name", "stockpilot-eks",
                     "--update-id", update["id"])["update"]
        if status["status"] == "Successful":
            break
        if status["status"] in ("Failed", "Cancelled"):
            raise SystemExit(f"Update stopped: {status.get('errors', [])}")
        time.sleep(5)
    else:
        raise SystemExit("Update still pending; inspect status before continuing.")
    print("AWS endpoint access updated.")
else:
    print("Current CloudShell IP is already allowed.")
PY
aws eks update-kubeconfig --name stockpilot-eks >/dev/null
kubectl --request-timeout=20s get nodes
