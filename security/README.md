# Security gates

The attached homework also requires SAST, SCA and secret scanning.

* Bandit 1.9.4 analyzes Python application syntax for security defects. Medium/high findings block quality. Low findings remain in JSON for review.
* Trivy filesystem secret scanning blocks detected credentials before builds.
* Trivy scans both final images and detected OS/language packages, blocking HIGH/CRITICAL findings including unfixed issues. The static frontend image's Node inventory contains only its root package; retained manifests are not proof that all bundled dependencies were scanned.
* A separate blocking `npm audit --audit-level=high --include=dev --json` checks the frontend lockfile's dependency graph, including build dependencies, against npm advisories. The report is archived as `frontend-sca.json`; HIGH/CRITICAL findings or audit-command errors fail quality before image builds.
* Reports are retained as Actions artifacts and allowlisted evidence. No suppression file, exit-zero or continue-on-error bypass is configured.

Run `bandit -r backend/app -ll -f json -o /tmp/bandit.json` and `trivy fs --scanners secret --exit-code 1 .`. A clean result describes this scan and database version, not an assurance that software has no vulnerabilities. Review reports and update dependencies regularly. Never paste credentials into manifests or screenshots.

## Actual blocked scan and remediation

Run [38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) scanned both images. Frontend Alpine/Node dependency results had zero HIGH/CRITICAL entries. Backend Python libraries were clean at that threshold, but Debian 13.7 OS packages caused a genuine failure. Publication was blocked. The report included CVE-2026-76642 in util-linux-derived packages (installed 2.41.5); its distro FixedVersion field was empty. The [upstream advisory](https://github.com/util-linux/util-linux/security/advisories/GHSA-m25x-3hj9-m26f) describes privileged mount post-hooks running despite a failed helper; upstream patched releases include 2.41.6/2.42.3. Other findings affected ncurses, systemd, ACL and Perl base packages.

We replaced the runtime with a maintained Python Alpine base, removing the Debian package set, and retained the blocking scan with unfixed findings included. Binary musllinux wheels support Psycopg/Pydantic on the new libc; real Compose/PostgreSQL/browser checks must pass again. This is an actual runtime change, not deleting package metadata or suppressing CVEs. Subsequent run [39000262612](https://github.com/not-so-shubh/devops-project/actions/runs/39000262612) passed both image scans: backend Alpine 3.24.2 (38 OS packages plus Python inventory) and frontend Alpine/Node inventory had zero HIGH/CRITICAL entries. The earlier scan remains documented as failed. See [blocked findings summary](../docs/evidence/trivy-backend-blocked-summary.json) and the actual JSON reports on the run evidence branch.

Secret scan evidence retains rule IDs, severities and file/line locations while stripping matched credential values and code snippets before artifact upload. Sanitization never changes Trivy’s blocking exit status. The redaction regression check also verifies that finding severity and count remain intact.

For the written rubric response, timed student explanations, current source-pinned reports and five instructor questions, see [TRIVY-EXPLANATION.md](../docs/TRIVY-EXPLANATION.md). Personal explanation remains READY FOR DEMO until the student demonstrates understanding.

## Later frontend package fix

Run [39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226) blocked frontend publication on HIGH CVE-2026-77214 in `libexpat 2.8.5-r0`; the report identifies `2.9.0-r0` as fixed. The Dockerfile now installs `libexpat>=2.9.0-r0` from the same supported Alpine repository during the build and restores runtime UID 101. No advisory is ignored and the HIGH/CRITICAL gate is unchanged. The remediation commit must pass its own full scans, Compose and cluster checks; use its actual evidence branch to verify the result. [Retained finding](../docs/evidence/trivy-frontend-blocked-summary.json).

Remediation verified: [run 39070661297](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297), source `710d1460abc480d8b19e2b98f648a9a5c1c23339`, passed both image scans and the full Compose/Kubernetes/monitoring/Flux regression. Its frontend build log confirms the upgrade to 2.9.0-r0, and the public image receipt confirms runtime UID 101.

## Subsequent libx11 gate failure and repair — 22 October 2026

Source `228cccd843c65b2e9dccbe5452d980a00b889a75`, [run 39694461786](https://github.com/not-so-shubh/devops-project/actions/runs/39694461786), passed quality, infrastructure, Compose and the backend image scan. The frontend scan reported **HIGH CVE-2026-88806** in **libx11 1.8.13-r0**, with **1.8.14-r0** as FixedVersion. Publication and Kubernetes jobs were skipped. [Source-pinned blocked finding](../docs/evidence/trivy-frontend-libx11-blocked-summary.json).

The frontend Dockerfile now requires `libx11>=1.8.14-r0` alongside the existing libexpat fix, from the same supported Alpine repository, and restores UID 101. The [official Alpine package page](https://pkgs.alpinelinux.org/package/v3.24/main/x86_64/libx11) lists the fixed package. [Red Hat's advisory](https://access.redhat.com/security/cve/cve-2026-88806) describes the upstream XKB-reply heap overflow; the project finding and package version are established by its actual Trivy report. No advisory suppression, reduced severity threshold, `ignore-unfixed` change or exit-zero bypass was added. The source's own complete CI run must establish the repaired image result; each main run archives its reports on `evidence/<source-sha>`.
