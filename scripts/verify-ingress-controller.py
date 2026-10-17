"""Check the pinned Traefik chart's actual Service type, not an ignored values key."""

import sys

import yaml

objects = [obj for obj in yaml.safe_load_all(open(sys.argv[1])) if obj]
services = [obj for obj in objects if obj.get("kind") == "Service"]
assert services and all(service["spec"]["type"] == "ClusterIP" for service in services)
assert any(
    obj.get("kind") == "IngressClass" and obj["metadata"]["name"] == "traefik" for obj in objects
)
print("PASS: Traefik Service is ClusterIP for kind; traefik IngressClass exists")
