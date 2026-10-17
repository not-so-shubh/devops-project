"""Create durable GHCR read credentials without shell arguments or a secret file."""

import base64
import getpass
import json
import subprocess

username = input("GitHub username with package read access: ").strip()
if not username:
    raise SystemExit("Username required")
token = getpass.getpass("Durable read:packages token (not an Actions job token): ")
if not token:
    raise SystemExit("Token required")
config = {"auths": {"ghcr.io": {"auth": base64.b64encode(f"{username}:{token}".encode()).decode()}}}
secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {"name": "ghcr-pull", "namespace": "stockpilot"},
    "type": "kubernetes.io/dockerconfigjson",
    "data": {".dockerconfigjson": base64.b64encode(json.dumps(config).encode()).decode()},
}
subprocess.run(
    ["kubectl", "apply", "--server-side", "-f", "-"],
    input=json.dumps(secret),
    text=True,
    check=True,
)
print(
    "Created stockpilot/ghcr-pull. Confirm actual package pull access and rotate credentials regularly."
)
