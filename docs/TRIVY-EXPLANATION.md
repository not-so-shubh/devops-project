# Explain StockPilot's image security gate

## Subsequent libx11 gate failure and repair — 22 October 2026

Source `228cccd843c65b2e9dccbe5452d980a00b889a75`, [run 39694461786](https://github.com/not-so-shubh/devops-project/actions/runs/39694461786), passed quality, infrastructure, Compose and the backend image scan. The frontend scan reported **HIGH CVE-2026-88806** in **libx11 1.8.13-r0**, with **1.8.14-r0** as FixedVersion. Publication and Kubernetes jobs were skipped. [Source-pinned blocked finding](evidence/trivy-frontend-libx11-blocked-summary.json).

The frontend Dockerfile now requires `libx11>=1.8.14-r0` alongside the existing libexpat fix, from the same supported Alpine repository, and restores UID 101. The [official Alpine package page](https://pkgs.alpinelinux.org/package/v3.24/main/x86_64/libx11) lists the fixed package. [Red Hat's advisory](https://access.redhat.com/security/cve/cve-2026-88806) describes the upstream XKB-reply heap overflow; the project finding and package version are established by its actual Trivy report. No advisory suppression, reduced severity threshold, `ignore-unfixed` change or exit-zero bypass was added. The source's own complete CI run must establish the repaired image result; each main run archives its reports on `evidence/<source-sha>`.

A useful personal explanation is: a later build exposed a new library finding in a digest-pinned base, so the unchanged gate stopped promotion. The fix updates the affected OS package and must pass scans and runtime regression again. A historical clean scan is not a permanent security guarantee.

## Historical separately verified scan — 18 October 2026

Source `cf87b82b40151d0c21c2e03740451a1a9ed2c649` completed [run 39115536536](https://github.com/not-so-shubh/devops-project/actions/runs/39115536536) successfully. Its actual [backend](https://github.com/not-so-shubh/devops-project/blob/405b839cd453bff6086a33b1f3ce4e68c19b3384/docs/evidence/trivy-backend.json) and [frontend](https://github.com/not-so-shubh/devops-project/blob/405b839cd453bff6086a33b1f3ce4e68c19b3384/docs/evidence/trivy-frontend.json) reports were independently inspected: zero HIGH/CRITICAL findings at the unchanged blocking threshold. The separate [full frontend lockfile audit](https://github.com/not-so-shubh/devops-project/blob/405b839cd453bff6086a33b1f3ce4e68c19b3384/docs/evidence/frontend-sca.json) covered 124 dependencies, including development/build dependencies, with zero reported vulnerabilities. A filtered image report does not claim absence of every lower-severity issue or every possible application defect.

Required short explanation: Trivy scanned the backend and frontend image OS packages and supported application dependencies for known vulnerabilities. Both current reports contained no HIGH or CRITICAL findings, so the security gate allowed promotion. This is a scan-time inventory/database result, not a guarantee against logic bugs, misconfiguration or future CVEs.

The historical finding/remediation explanation below remains source-pinned. Personal student understanding still requires the student's own explanation.


Reviewed source: `710d1460abc480d8b19e2b98f648a9a5c1c23339`; [successful run 39070661297](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297). This is preparation for M6.3; the student must demonstrate understanding personally.

## Subsequent rebuild: frontend libexpat finding

The later [run 39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226), source `bd407322dda34ebb5d9b7a0ca05ff57106f13382`, correctly **failed** its frontend scan. Trivy reported one HIGH finding: **CVE-2026-77214**, `libexpat 2.8.5-r0`, fixed version `2.9.0-r0`. Backend passed; both image publication and Kubernetes deployment were skipped because the gate blocked promotion. This does not invalidate the older timestamped clean reports; it demonstrates why every rebuild needs a fresh scan.

The frontend Dockerfile now requires `libexpat>=2.9.0-r0` from the same Alpine 3.24 repository, whose [official package page](https://pkgs.alpinelinux.org/package/v3.24/main/x86_64/libexpat) lists that fixed release. The build temporarily uses root to install the update, then explicitly returns to runtime UID 101. The base digest, dependency inventory and blocking Trivy settings remain in place. The remediation source `710d1460abc480d8b19e2b98f648a9a5c1c23339` passed the full [run 39070661297](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297). The build log confirms `2.8.5-r0 -> 2.9.0-r0`; both final reports contain zero HIGH/CRITICAL findings, both images were published as non-root runtimes, and Compose/Ingress/monitoring/Flux checks passed. The failed `bd40732` image was not published by its failed run. [Exact retained finding](evidence/trivy-frontend-blocked-summary.json) · [Original full report](https://github.com/not-so-shubh/devops-project/blob/fc1966161ec1394c42a9c2c4db9c3ffb2668181f/docs/evidence/trivy-frontend.json).

The upstream issue concerns XML_ParseBuffer advancing a buffer pointer beyond its capacity and reading uninitialized/out-of-bounds heap data. It is not evidence of a demonstrated remote compromise of StockPilot. Vendors can rate the same advisory differently; describe the HIGH severity actually reported by this project's Trivy run. [Upstream project fix](https://github.com/libexpat/libexpat/commit/4d9b1c499ecb66323260a7274edcf86c5eab0517).

## Required written explanation

Trivy inspects final backend/frontend images for known OS/library vulnerabilities and blocks HIGH or CRITICAL findings, including unfixed ones. Older reviewed images were clean at that threshold, but a later rebuild correctly blocked frontend libexpat CVE-2026-77214; the Dockerfile now requires the fixed package, and the source-pinned remediation run passed both scans and runtime checks. A clean result is specific to the image, inventory, database and scan time, not proof of complete security.

## 30-second student explanation

“Our pipeline scans both images before publishing. It previously blocked a Debian backend, which we replaced and retested. A later rebuild caught HIGH CVE-2026-77214 in frontend libexpat 2.8.5, so we required fixed version 2.9.0 and reran the same gate. I check the fix's own report before calling it clean. This shows why yesterday's clean scan is not a permanent security guarantee.”

## Two-minute technical explanation

“Trivy inventories detected OS packages and language dependencies in the actual image, then compares them with advisories. We scan both the Python backend and Nginx frontend. The static frontend image contains only a root Node package in its detected inventory, so CI also runs a blocking npm lockfile audit including build dependencies. Retaining package manifests alone does not prove full dependency coverage. The image scan uses an exit code of one for HIGH and CRITICAL findings and has no ignore-unfixed bypass. Publishing waits for these gates.

“HIGH and CRITICAL are severity categories. In CVSS v3, HIGH spans 7.0–8.9 and CRITICAL spans 9.0–10.0. Severity is not a statement that an exploit has occurred or that every affected package is reachable in this container. Trivy may use a vendor's severity assessment; the report and advisory determine which assessment applies.

“Our original backend scan found 44 HIGH package findings and zero CRITICAL findings in Debian 13.7. These are package/advisory occurrences, not 44 distinct CVEs. One real example is CVE-2026-76642, reported against util-linux-derived packages with installed version 2.41.5. The upstream advisory describes privileged mount post-hooks running even when an external helper fails. It is a local privilege escalation issue with prerequisites; we did not demonstrate remote exploitation of our API. The distro report had no FixedVersion value. Upstream lists patched releases 2.41.6 and 2.42.3, which is different from a confirmed patched Debian package being available.

“We replaced the Debian runtime with a maintained Python Alpine image, removing that affected Debian package set. We did not hide package metadata or suppress the CVE. Since Alpine uses musl, we reran real PostgreSQL, container and browser checks. Both current image reports have zero findings at the configured HIGH/CRITICAL threshold. We still need dependency refreshes, secrets and code scanning, runtime hardening, access control and future rescans.”

## Actual findings and remediation

| Evidence | Observed result |
|---|---|
| [Blocked run 38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) | Backend image `800b7b72c86042474e2245c529ecf798d7267d0b`: Debian 13.7, 44 HIGH package findings, zero CRITICAL. Backend Python findings were clean at this threshold; the OS findings failed the job. |
| [Retained blocked summary](evidence/trivy-backend-blocked-summary.json) | Includes actual package names, installed versions, advisory IDs and empty distro FixedVersion values. Other findings included ncurses, systemd, ACL and Perl packages. |
| [util-linux upstream advisory](https://github.com/util-linux/util-linux/security/advisories/GHSA-m25x-3hj9-m26f) | CVE-2026-76642, HIGH, CVSS 7.8; upstream patched versions 2.41.6 and 2.42.3. |
| [Backend report](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/trivy-backend.json) | `ghcr.io/not-so-shubh/stockpilot-backend:710d1460abc480d8b19e2b98f648a9a5c1c23339`, scanned 2026-10-17 21:25 UTC; Alpine 3.24.2 plus Python inventory; zero HIGH/CRITICAL. |
| [Frontend report](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/trivy-frontend.json) | `ghcr.io/not-so-shubh/stockpilot-frontend:710d1460abc480d8b19e2b98f648a9a5c1c23339`, scanned 2026-10-17 21:25 UTC; Alpine 3.24.2 plus Node inventory; zero HIGH/CRITICAL. |
| [Workflow](../.github/workflows/ci-cd.yml), [runtime Dockerfile](../backend/Dockerfile) | Final images scanned before promotion; non-root runtime and digest-pinned base; security failure remains blocking. |

The JSON reports are filtered by the configured severity threshold. Do not interpret their zero HIGH/CRITICAL result as a statement that every LOW, MEDIUM or UNKNOWN vulnerability was assessed and absent.

The separate npm report `frontend-sca.json` includes advisory results for the lockfile graph; `--audit-level=high` sets its failure threshold rather than filtering lower-severity output. Check this report on the final run's evidence branch. The older reviewed run predates this additional gate, so its clean Trivy report must not be presented as lockfile-wide SCA proof. Primary references: [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/) and [Trivy Node.js coverage](https://trivy.dev/docs/latest/coverage/language/nodejs/).

## Five likely instructor questions

| Question | Answer |
|---|---|
| Why scan images rather than only requirements.txt? | The runtime contains OS libraries and other packages too. A clean Python dependency list did not prevent the earlier Debian OS failure. |
| Did you fix CVE-2026-76642 by upgrading Debian util-linux? | No. We changed the runtime distribution and removed that Debian package set, then rescanned and retested compatibility. The upstream fixed-version list is not proof we installed a patched Debian package. |
| Why block an unfixed finding? | That is the project's gate. We choose a maintained alternative or wait for a fix rather than silently exempting it. |
| Is HIGH the same as an exploitable remote attack? | No. Severity, exposure and exploitability differ. This advisory describes local privileged mount behavior; the scan identifies a package match, not a successful API exploit. |
| Can a green scan guarantee security? | No. It depends on known advisories and detected inventory at scan time. Logic flaws, authorization, deployment configuration and future CVEs need separate controls. |

Further primary references: [Trivy severity selection](https://trivy.dev/docs/latest/scanner/vulnerability/), [FIRST CVSS v3.1 severity ranges](https://www.first.org/cvss/v3.1/specification-document#Qualitative-Severity-Rating-Scale).
