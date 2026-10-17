"""Prove anonymous GHCR access, image source revision and all layer availability."""

import concurrent.futures
import json
import re
import sys
import urllib.request
from pathlib import Path

sha, component = sys.argv[1:]
assert re.fullmatch(r"[a-f0-9]{40}", sha) and component in {"backend", "frontend"}
repository = f"not-so-shubh/stockpilot-{component}"
with urllib.request.urlopen(
    f"https://ghcr.io/token?service=ghcr.io&scope=repository:{repository}:pull", timeout=20
) as response:
    token = json.load(response)["token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.docker.distribution.manifest.v2+json,application/vnd.oci.image.manifest.v1+json",
}
base = f"https://ghcr.io/v2/{repository}"
request = urllib.request.Request(f"{base}/manifests/{sha}", headers=headers)
with urllib.request.urlopen(request, timeout=20) as response:
    manifest = json.load(response)
    digest = response.headers["Docker-Content-Digest"]
with urllib.request.urlopen(
    urllib.request.Request(f"{base}/blobs/{manifest['config']['digest']}", headers=headers),
    timeout=20,
) as response:
    config = json.load(response)["config"]
assert config["Labels"]["org.opencontainers.image.revision"] == sha
assert (
    config["Labels"]["org.opencontainers.image.source"]
    == "https://github.com/not-so-shubh/devops-project"
)
assert config["User"].split(":")[0] in {"10001", "101"}


def available(layer):
    request = urllib.request.Request(
        f"{base}/blobs/{layer['digest']}", headers=headers, method="HEAD"
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.status == 200


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(available, manifest["layers"]))
assert all(results)
proof = {
    "image": f"ghcr.io/{repository}:{sha}",
    "manifest_digest": digest,
    "anonymous_manifest": True,
    "all_layers_anonymously_accessible": True,
    "layer_count": len(results),
    "source_revision": sha,
    "runtime_user": config["User"],
}
Path("docs/evidence").mkdir(parents=True, exist_ok=True)
Path(f"docs/evidence/ghcr-{component}.json").write_text(json.dumps(proof, indent=2) + "\n")
print(json.dumps(proof, indent=2))
