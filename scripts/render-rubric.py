"""Render the complete official rubric audit from its maintained JSON records."""

import json
from pathlib import Path

data = json.loads(Path("docs/rubric-audit.json").read_text())
rows = data["criteria"]
assert len(rows) == 46 and sum(r["points"] for r in rows) == 100
statuses = ["VERIFIED", "READY FOR DEMO", "BLOCKED", "EXCLUDED"]
assert all(r["status"] in statuses and r["source_sha"] for r in rows)
lines = [
    "# Complete rubric verification audit",
    "",
    f"Official source: {data['source']}",
    f"Reference reviewed: `{data['reference_commit']}`. Updated: {data['updated']}.",
    "",
    f"Verified project source: `{data['verified_source_sha']}`. "
    f"[Complete CI run]({data['verified_run_url']}). "
    f"Evidence commit: `{data['evidence_commit']}`.",
    "",
    data["note"],
    "",
    "| Module / criterion | Points | Status | Implemented feature and check | Actual result | Evidence | Source SHA | Remaining action |",
    "|---|---:|---|---|---|---|---|---|",
]
for r in rows:

    def cell(x):
        return str(x).replace("|", "\\|").replace("\n", " ")

    lines.append(
        "| "
        + " | ".join(
            map(
                cell,
                [
                    r["id"] + " " + r["criterion"],
                    r["points"],
                    r["status"],
                    r["implementation"] + "; " + r["verification"],
                    r["actual_result"],
                    r["evidence"],
                    "`" + r["source_sha"] + "`",
                    r["blocker"] or "None for this criterion",
                ],
            )
        )
        + " |"
    )
lines += [
    "",
    "## Module coverage of verified criteria",
    "",
    "These are rubric points attached to verified criteria, not a predicted or awarded grade.",
    "",
    "| Module | Available | VERIFIED | READY FOR DEMO | BLOCKED | EXCLUDED |",
    "|---|---:|---:|---:|---:|---:|",
]
for n in range(1, 11):
    selected = [r for r in rows if r["module"] == f"M{n}"]
    total = sum(r["points"] for r in selected)
    values = [sum(r["points"] for r in selected if r["status"] == s) for s in statuses]
    lines.append(f"| M{n} | {total} | " + " | ".join(map(str, values)) + " |")
totals = [sum(r["points"] for r in rows if r["status"] == s) for s in statuses]
lines.append("| **Total** | **100** | " + " | ".join(map(str, totals)) + " |")
lines += [
    "",
    "A successful kind deployment proves Kubernetes portability. It does not prove AWS provisioning, an account-dependent Terraform plan, destruction, or the student’s final live presentation.",
    "",
    "VERIFIED: actual executed evidence checked. READY FOR DEMO: preparation/technical chain available, but the student must explain or present personally. BLOCKED: requires remaining authorization, external access or execution. EXCLUDED: Student action — excluded from this task (official form only).",
    "",
    "See [SUBMISSION.md](SUBMISSION.md) for remaining criteria and screenshot formats; [AWS-EKS-CAPTURE-REVIEW.md](AWS-EKS-CAPTURE-REVIEW.md) records the inspected real AWS evidence, and [AWS-EKS-RUNTIME-VERIFICATION.md](AWS-EKS-RUNTIME-VERIFICATION.md) records lifecycle and CI access limits. [AWS-CLEANUP-VERIFICATION.md](AWS-CLEANUP-VERIFICATION.md) records the completed approved teardown.",
    "",
]
Path("docs/RUBRIC-CHECKLIST.md").write_text("\n".join(lines))
print("Rendered all 46 criteria, totaling 100 points.")
