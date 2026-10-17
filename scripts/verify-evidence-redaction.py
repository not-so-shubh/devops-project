"""Regression check: escaped Docker build strings must remain valid JSON evidence."""

import importlib.util
import json

spec = importlib.util.spec_from_file_location("redactor", "scripts/redact-evidence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = {
    "created_by": 'RUN if echo "$HASH */tmp/key"; then cat /home/runner/work/job/file; fi',
    "count": 44,
    "coverage": 97.67,
    "targets": [{"ip": "10.42.1.20", "health": "up", "loopback": "127.0.0.1"}],
    "Vulnerabilities": [{"VulnerabilityID": "CVE-2026-76642", "Severity": "HIGH"}],
}
encoded = json.dumps(module.redact_json(original))
result = json.loads(encoded)
assert "/tmp/key" not in encoded and "/home/runner" not in encoded
assert "10.42.1.20" not in encoded
assert result["count"] == 44 and result["coverage"] == 97.67
assert result["Vulnerabilities"] == original["Vulnerabilities"]
assert result["targets"][0]["health"] == "up"
assert result["targets"][0]["loopback"] == "127.0.0.1"
print("PASS: redaction preserves valid JSON, finding severity, counts and metrics")

spec = importlib.util.spec_from_file_location("secrets_report", "scripts/sanitize-secret-report.py")
secret_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(secret_module)
canary = "CANARY_VALUE_MUST_BE_REMOVED"
report = {
    "Results": [
        {
            "Target": "example.py",
            "Secrets": [
                {
                    "RuleID": "canary-rule",
                    "Severity": "HIGH",
                    "StartLine": 7,
                    "Match": canary,
                    "Code": {"content": canary},
                }
            ],
        }
    ]
}
clean = secret_module.safe_report(report)
assert canary not in json.dumps(clean)
assert clean["Results"][0]["Secrets"][0] == {
    "RuleID": "canary-rule",
    "Severity": "HIGH",
    "StartLine": 7,
}
print("PASS: secret evidence preserves finding severity/location and excludes matched credentials")
