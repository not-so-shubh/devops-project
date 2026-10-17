"""Render the complete official rubric audit from its maintained JSON records."""

import json
from pathlib import Path

data = json.loads(Path("docs/rubric-audit.json").read_text())
rows = data["criteria"]
assert len(rows) == 46 and sum(r["points"] for r in rows) == 100
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
    "| Criterion | Points | Implemented file or feature | Verification command/check | Actual result | Evidence | Remaining blocker |",
    "|---|---:|---|---|---|---|---|",
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
                    r["implementation"],
                    r["verification"],
                    r["status"] + ": " + r["actual_result"],
                    r["evidence"],
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
    "| Module | Available | Attached to verified criteria | Pending |",
    "|---|---:|---:|---:|",
]
for n in range(1, 11):
    selected = [r for r in rows if r["module"] == f"M{n}"]
    total = sum(r["points"] for r in selected)
    passed = sum(r["points"] for r in selected if r["status"] == "PASS")
    lines.append(f"| M{n} | {total} | {passed} | {total - passed} |")
lines += [
    "",
    "A successful kind deployment proves Kubernetes portability. It does not prove AWS provisioning, an account-dependent Terraform plan, destruction, or the student’s final live presentation.",
    "",
    "See [SUBMISSION.md](SUBMISSION.md) for the seven open criteria and required final screenshot formats.",
    "",
]
Path("docs/RUBRIC-CHECKLIST.md").write_text("\n".join(lines))
print("Rendered all 46 criteria, totaling 100 points.")
