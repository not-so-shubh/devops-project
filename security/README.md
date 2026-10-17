# Security gates

The attached homework also requires SAST, SCA and secret scanning.

* Bandit 1.9.4 analyzes Python application syntax for security defects. Medium/high findings block quality. Low findings remain in JSON for review.
* Trivy filesystem secret scanning blocks detected credentials before builds.
* Trivy scans both final images, OS packages and application libraries, and blocks HIGH/CRITICAL findings including unfixed issues. Frontend lockfiles are retained outside the served document root so JavaScript dependencies remain inspectable.
* Reports are retained as Actions artifacts and allowlisted evidence. No suppression file, exit-zero or continue-on-error bypass is configured.

Run `bandit -r backend/app -ll -f json -o /tmp/bandit.json` and `trivy fs --scanners secret --exit-code 1 .`. A clean result describes this scan and database version, not an assurance that software has no vulnerabilities. Review reports and update dependencies regularly. Never paste credentials into manifests or screenshots.
