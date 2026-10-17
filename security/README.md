# Security gates

The attached homework also requires SAST, SCA and secret scanning.

* Bandit 1.9.4 analyzes Python application syntax for security defects. Medium/high findings block quality. Low findings remain in JSON for review.
* Trivy filesystem secret scanning blocks detected credentials before builds.
* Trivy scans both final images, OS packages and application libraries, and blocks HIGH/CRITICAL findings including unfixed issues. Frontend lockfiles are retained outside the served document root so JavaScript dependencies remain inspectable.
* Reports are retained as Actions artifacts and allowlisted evidence. No suppression file, exit-zero or continue-on-error bypass is configured.

Run `bandit -r backend/app -ll -f json -o /tmp/bandit.json` and `trivy fs --scanners secret --exit-code 1 .`. A clean result describes this scan and database version, not an assurance that software has no vulnerabilities. Review reports and update dependencies regularly. Never paste credentials into manifests or screenshots.

## Actual blocked scan and remediation

Run [38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) scanned both images. Frontend Alpine/Node dependency results had zero HIGH/CRITICAL entries. Backend Python libraries were clean at that threshold, but Debian 13.7 OS packages caused a genuine failure. Publication was blocked. The report included CVE-2026-76642 in util-linux-derived packages (installed 2.41.5); its distro FixedVersion field was empty. The [upstream advisory](https://github.com/util-linux/util-linux/security/advisories/GHSA-m25x-3hj9-m26f) describes privileged mount post-hooks running despite a failed helper; upstream patched releases include 2.41.6/2.42.3. Other findings affected ncurses, systemd, ACL and Perl base packages.

We replaced the runtime with a maintained Python Alpine base, removing the Debian package set, and retained the blocking scan with unfixed findings included. Binary musllinux wheels support Psycopg/Pydantic on the new libc; real Compose/PostgreSQL/browser checks must pass again. This is an actual runtime change, not deleting package metadata or suppressing CVEs. The subsequent scan result is recorded separately; do not describe the earlier scan as clean.
