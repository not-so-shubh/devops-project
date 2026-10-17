"""Check rendered chart wiring in addition to Helm's syntax/schema validation."""

import sys

import yaml

objects = [o for o in yaml.safe_load_all(open(sys.argv[1])) if o and o.get("kind")]
by_kind = {}
for obj in objects:
    by_kind.setdefault(obj["kind"], {})[obj["metadata"]["name"]] = obj
services = by_kind["Service"]
for name, port in [("backend", 8000), ("frontend", 8080)]:
    service = services[name]["spec"]
    assert service["type"] == "ClusterIP"
    assert service["ports"][0]["port"] == port
    deployment = by_kind["Deployment"][f"stockpilot-{name}"]["spec"]
    labels = deployment["template"]["metadata"]["labels"]
    assert all(labels.get(k) == v for k, v in service["selector"].items())
    container = deployment["template"]["spec"]["containers"][0]
    assert container["ports"][0]["containerPort"] == port
    assert container["securityContext"]["readOnlyRootFilesystem"]
    assert container["readinessProbe"] and container["livenessProbe"]
    assert container["resources"]["requests"]["cpu"]
    assert deployment["template"]["spec"]["securityContext"]["runAsNonRoot"]
for path in by_kind["Ingress"]["stockpilot"]["spec"]["rules"][0]["http"]["paths"]:
    target = path["backend"]["service"]
    assert target["port"]["number"] == services[target["name"]]["spec"]["ports"][0]["port"]
hpa = by_kind["HorizontalPodAutoscaler"]["stockpilot-backend"]["spec"]
assert hpa["minReplicas"] >= 2 and hpa["maxReplicas"] > hpa["minReplicas"]
monitor = by_kind["ServiceMonitor"]["stockpilot-backend"]["spec"]
assert monitor["endpoints"][0]["port"] == "http"
assert all(
    services["backend"]["metadata"]["labels"].get(k) == v
    for k, v in monitor["selector"]["matchLabels"].items()
)
assert by_kind["StatefulSet"]["stockpilot-postgres"]["spec"]["volumeClaimTemplates"]
assert by_kind["Job"]
print(
    f"PASS: {len(objects)} resources; selectors, ports, probes, storage, HPA, migration Job and ServiceMonitor wiring"
)
