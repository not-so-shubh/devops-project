# Explain the Trivy gate

[Documentation hub](README.md) · [Security controls/history](../security/README.md) · [Instructor questions](INSTRUCTOR-QA.md)

This is preparation for the student's personal M6.3 explanation. Written material and a slide upload do not establish that the student understands the result.

## Required short explanation

Trivy scanned the final backend and frontend container images for known OS and supported application-dependency vulnerabilities. In [source `8944da7`'s complete successful run](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574), both reports contained zero HIGH/CRITICAL findings after the frontend libx11 package was updated to the fixed version. The unchanged gate stops promotion when that threshold is reached, and its clean result describes that particular source and vulnerability-database timestamp.

## One actual CVE to explain

| Item | Observed project fact |
|---|---|
| Advisory | CVE-2026-88806, HIGH, libX11 handling of malicious XKB replies |
| Failed source/run | `228cccd843c65b2e9dccbe5452d980a00b889a75`, [39694461786](https://github.com/not-so-shubh/devops-project/actions/runs/39694461786) |
| Installed version | `libx11 1.8.13-r0` |
| Report's fixed version | `1.8.14-r0` |
| Gate behavior | Frontend scan failed; publication and Kubernetes jobs skipped |
| Code repair | [`frontend/Dockerfile`](../frontend/Dockerfile) requires `libx11>=1.8.14-r0` from the same supported Alpine repository |
| Verified result | [Frontend report](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/trivy-frontend.json) lists `1.8.14-r0` with zero HIGH/CRITICAL findings; both image gates and complete runtime regression passed |

[Original blocked summary](evidence/trivy-frontend-libx11-blocked-summary.json) · [Original full blocked report](https://github.com/not-so-shubh/devops-project/blob/3789ce85e07867bae31f437aae94c5f5cd968e5f/docs/evidence/trivy-frontend.json) · [Advisory context](https://access.redhat.com/security/cve/cve-2026-88806).

## A 30-second rehearsal

Explain in your own words: a digest-pinned image still contains versioned operating-system packages. A later scan found a HIGH libx11 issue, so the pipeline stopped publishing. The Dockerfile installed the fixed supported package and returned to non-root UID 101. The new source passed the same blocking scan and full Compose/Kubernetes checks. The result is point-in-time evidence, so future builds still scan.

## A two-minute explanation

1. Open the failed source's actual report. Identify the CVE, package, installed/fixed versions and severity.
2. Show the failed `build-security (frontend)` job and skipped promotion jobs. A backend pass does not promote the failed frontend.
3. Show the package requirement in the Dockerfile. No suppression file, `ignore-unfixed` relaxation, exit-zero or metadata deletion was added.
4. Open the repaired source's own reports, GHCR source receipts and complete runtime checks. The build restores runtime UID 101.
5. Explain scope: image OS/dependency scanning differs from Bandit SAST, secret scanning, full npm lockfile SCA, business-logic tests and operational access controls.

## Questions to rehearse

| Question | Accurate answer |
|---|---|
| Why scan a pinned base? | The digest makes the starting bytes repeatable; advisories and supported package fixes change over time. |
| Did the project suppress this finding? | No. It required the fixed package and retained the original HIGH/CRITICAL gate. |
| Does zero HIGH/CRITICAL mean no vulnerability exists? | It records that threshold for this source/database. Other severities, new advisories and logic flaws need separate assessment. |
| Was every frontend dependency proved clean by the image report? | No. A separate full lockfile audit, including dev/build dependencies, reported zero vulnerabilities across 124 dependencies in this baseline. |
| Were blocked images published? | The failed run's publication and cluster jobs were skipped. Repaired images required their own successful run. |

## Preserved earlier history

The earlier libexpat CVE-2026-77214 failure/fix and backend Debian-to-Alpine remediation remain in [security history](../security/README.md#actual-failed-scans-and-remediation), their retained summaries and immutable reports. [The pre-polish full explanation](https://github.com/not-so-shubh/devops-project/blob/8944da7ddf2be0845a593c2f65482eb922e6d9f7/docs/TRIVY-EXPLANATION.md) preserves the longer dated narrative. The application's tests still verify correctness independently of scan results.
