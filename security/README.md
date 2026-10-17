# Security gates

The attached homework also requires SAST, SCA and secret scanning.

* Bandit 1.9.4 analyzes Python application syntax for security defects. Medium/high findings block quality. Low findings remain in JSON for review.
* Trivy filesystem secret scanning blocks detected credentials before builds.
* Trivy scans both final images, OS packages and application libraries, and blocks HIGH/CRITICAL findings including unfixed issues. Frontend lockfiles are retained outside the served document root so JavaScript dependencies remain inspectable.
* Reports are retained as Actions artifacts and allowlisted evidence. No suppression file, exit-zero or continue-on-error bypass is configured.

Run `bandit -r backend/app -ll -f json -o /tmp/bandit.json` and `trivy fs --scanners secret --exit-code 1 .`. A clean result describes this scan and database version, not an assurance that software has no vulnerabilities. Review reports and update dependencies regularly. Never paste credentials into manifests or screenshots.

## Actual blocked scan and remediation

Run [38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) scanned both images. Frontend Alpine/Node dependency results had zero HIGH/CRITICAL entries. Backend Python libraries were clean at that threshold, but Debian 13.7 OS packages caused a genuine failure. Publication was blocked. The report included CVE-2026-76642 in util-linux-derived packages (installed 2.41.5); its distro FixedVersion field was empty. The [upstream advisory](https://github.com/util-linux/util-linux/security/advisories/GHSA-m25x-3hj9-m26f) describes privileged mount post-hooks running despite a failed helper; upstream patched releases include 2.41.6/2.42.3. Other findings affected ncurses, systemd, ACL and Perl base packages.

We replaced the runtime with a maintained Python Alpine base, removing the Debian package set, and retained the blocking scan with unfixed findings included. Binary musllinux wheels support Psycopg/Pydantic on the new libc; real Compose/PostgreSQL/browser checks must pass again. This is an actual runtime change, not deleting package metadata or suppressing CVEs. Subsequent run [39000262612](https://github.com/not-so-shubh/devops-project/actions/runs/39000262612) passed both image scans: backend Alpine 3.24.2 (38 OS packages plus Python inventory) and frontend Alpine/Node inventory had zero HIGH/CRITICAL entries. The earlier scan remains documented as failed. See [blocked findings summary](../docs/evidence/trivy-backend-blocked-summary.json) and the actual JSON reports on the run evidence branch.

Secret scan evidence retains rule IDs, severities and file/line locations while stripping matched credential values and code snippets before artifact upload. Sanitization never changes Trivy’s blocking exit status. The redaction regression check also verifies that finding severity and count remain intact.

For the written rubric response, timed student explanations, current source-pinned reports and five instructor questions, see [TRIVY-EXPLANATION.md](../docs/TRIVY-EXPLANATION.md). Personal explanation remains READY FOR DEMO until the student demonstrates understanding.
