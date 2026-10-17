"""Summarize actual Trivy image JSON without substituting for its blocking exit code."""

import json
import sys
from pathlib import Path

reports = []
for filename in sys.argv[1:]:
    report = json.loads(Path(filename).read_text())
    results = report.get("Results", [])
    findings = [v for result in results for v in result.get("Vulnerabilities", [])]
    reports.append(
        {
            "image": report.get("ArtifactName"),
            "scanner": report.get("Metadata", {}).get("OS"),
            "targets": [
                {"type": r.get("Type"), "class": r.get("Class"), "target": r.get("Target")}
                for r in results
            ],
            "high": sum(v["Severity"] == "HIGH" for v in findings),
            "critical": sum(v["Severity"] == "CRITICAL" for v in findings),
            "findings": [
                {
                    k: v.get(k)
                    for k in [
                        "VulnerabilityID",
                        "PkgName",
                        "InstalledVersion",
                        "FixedVersion",
                        "Severity",
                    ]
                }
                for v in findings
            ],
        }
    )
print(json.dumps(reports, indent=2))
