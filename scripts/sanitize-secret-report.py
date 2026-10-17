"""Keep secret-finding evidence while omitting matched credentials and source snippets."""

import json
import sys
from pathlib import Path


def safe_report(report):
    fields = ["RuleID", "Category", "Severity", "Title", "StartLine", "EndLine"]
    return {
        "SchemaVersion": report.get("SchemaVersion"),
        "ArtifactName": report.get("ArtifactName"),
        "Redaction": "Matched values and code snippets omitted; finding identifiers, severity and locations retained",
        "Results": [
            {
                "Target": result.get("Target"),
                "Class": result.get("Class"),
                "Type": result.get("Type"),
                "Secrets": [
                    {key: finding[key] for key in fields if key in finding}
                    for finding in (result.get("Secrets") or [])
                ],
            }
            for result in (report.get("Results") or [])
        ],
    }


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/evidence/secrets.json")
    if path.exists():
        raw = path.read_text()
        # Remove the raw file first, so an invalid report cannot be uploaded by an always step.
        path.unlink()
        clean = safe_report(json.loads(raw))
        path.write_text(json.dumps(clean, indent=2) + "\n")
        count = sum(len(result["Secrets"]) for result in clean["Results"])
        print(f"Retained {count} secret finding(s); matching values and source snippets removed")
    else:
        print("No secret report was produced by this run")
