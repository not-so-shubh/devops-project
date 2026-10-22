# Security controls and evidence

[Documentation hub](../docs/README.md) · [Student Trivy explanation](../docs/TRIVY-EXPLANATION.md) · [Evidence](../docs/EVIDENCE.md)

## Blocking gates

| Gate | Scope and behavior |
|---|---|
| Ruff / frontend quality | Static checks before integration/build promotion |
| Bandit | Python application SAST; configured findings fail quality |
| Trivy secrets | Repository credential scanning; detected secrets fail quality |
| npm audit | Full frontend lockfile graph, including build/dev dependencies; HIGH/CRITICAL or command errors fail quality |
| Trivy images | Both final runtime images, OS/supported dependency inventory; HIGH/CRITICAL, including unfixed findings, block promotion |

There is no CVE suppression, `continue-on-error`, exit-zero workaround or weakened severity threshold. Secret evidence strips matched credential values/code while retaining finding severity/location; sanitization never changes the scanner's blocking status.

## Verified application baseline

[Source `8944da7`, run 39696800574](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574) passed all enabled jobs. [Backend scan](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/trivy-backend.json) and [frontend scan](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/trivy-frontend.json) have **zero HIGH/CRITICAL findings**. The frontend report inventories **libx11 1.8.14-r0**. The separate [full lockfile audit](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/frontend-sca.json) reports zero vulnerabilities across 124 dependencies.

A filtered image report is not proof that every bundled JavaScript dependency was inventoried; the separate lockfile gate covers that graph. Scan results describe known findings at the source/database timestamp. Logic flaws, future advisories and operational misconfiguration need their own checks.

## Actual failed scans and remediation

| Failed run | Finding | Repair and follow-up |
|---|---|---|
| [38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) | Backend Debian OS HIGH findings, including util-linux CVE-2026-76642 | Replaced the runtime with maintained Python Alpine and revalidated PostgreSQL/Compose/browser behavior; [retained summary](../docs/evidence/trivy-backend-blocked-summary.json) |
| [39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226) | Frontend HIGH CVE-2026-77214, libexpat 2.8.5-r0 | Required libexpat>=2.9.0-r0 in the supported Alpine release; [full green follow-up](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297) and [retained finding](../docs/evidence/trivy-frontend-blocked-summary.json) |
| [39694461786](https://github.com/not-so-shubh/devops-project/actions/runs/39694461786) | Frontend HIGH CVE-2026-88806, libx11 1.8.13-r0 | Required libx11>=1.8.14-r0; [full green follow-up](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574) and [retained finding](../docs/evidence/trivy-frontend-libx11-blocked-summary.json) |

The Dockerfile temporarily uses root for the supported package updates and restores UID 101. It does not remove package metadata to hide a finding. The libx11 advisory describes malicious XKB reply handling; [upstream advisory context](https://access.redhat.com/security/cve/cve-2026-88806) and [supported Alpine package](https://pkgs.alpinelinux.org/package/v3.24/main/x86_64/libx11) complement the project's actual scan. Historical clean scans remain historical; each later build must pass its own gate.

## Runtime and credential boundaries

Application runtimes are non-root/read-only, with dropped capabilities and no privilege escalation. Secrets, kubeconfig, AWS credentials, actual tfvars, state and plans stay outside Git. Kubernetes Secret base64 encoding alone is not encryption. The application has no login/RBAC; use synthetic data and add authentication, TLS, tested recovery and availability planning before business use.

The optional AWS OIDC job remains disabled because organization policy blocked provider access. No permanent-key bypass or overly broad trust change is part of this work. [AWS account boundary](../docs/AWS-READINESS.md).

For M6.3, the written explanation and rehearsal guide are prepared. The student must personally demonstrate understanding; a clean automated scan or uploaded PowerPoint does not assess that point.
