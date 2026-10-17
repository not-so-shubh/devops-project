# Evidence index and submission record

Only actual command output, real screenshots, and real run/resource links belong here. A configuration file is not evidence that an infrastructure resource exists. Review [all 46 official criteria](RUBRIC-CHECKLIST.md); the underlying records are in `rubric-audit.json`.

## Verified so far

| Evidence | Result | File or source |
|---|---|---|
| Local Pytest | 43 passed, one PostgreSQL-only test skipped; 98.83% | [pytest-local.txt](evidence/pytest-local.txt) |
| Actual PostgreSQL CI tests | 44 passed, including concurrent stock removal; 97.67% | [github-quality.txt](evidence/github-quality.txt), [quality job](https://github.com/not-so-shubh/devops-project/actions/runs/38997526583/job/117293235818) |
| Frontend quality and build | Lint, four utility tests and production build passed | [quality job](https://github.com/not-so-shubh/devops-project/actions/runs/38997526583/job/117293235818), [frontend-build.txt](evidence/frontend-build.txt) |
| Compose startup and HTTP integration | All services healthy; migration complete; non-root IDs checked; real proxy/API smoke passed | [github-compose-first-run.txt](evidence/github-compose-first-run.txt) |
| Terraform initialization and validation | Passed on real GitHub runner; offline topology test passed | [github-infrastructure.txt](evidence/github-infrastructure.txt) |
| Helm schema and wiring | Lint/template passed; 10 rendered resources and cross-resource wiring checked | [helm-lint.txt](evidence/helm-lint.txt), [helm-wiring.txt](evidence/helm-wiring.txt) |
| Git history | Public destination with more than ten meaningful commits | [main history](https://github.com/not-so-shubh/devops-project/commits/main/) |

First run [38997526583](https://github.com/not-so-shubh/devops-project/actions/runs/38997526583) failed full browser acceptance after passing the stack and HTTP checks. The mobile scroller containment defect was corrected, and all four Compose browser tests passed in run 38999948371 and again after the runtime base change in run 39000262612. The earlier runs must not be presented as green pipelines. Both latter image scans and GHCR publication passed; Kubernetes verification remains tracked independently.

## Durable CI evidence

Runs archive an explicit allowlist of screenshots, test/Compose/Helm/Kubernetes outputs, actual Trivy JSON, Prometheus target/query responses and Grafana screenshots on `evidence/<source-sha>`. `ci-run.json` records the source SHA, run URL, and actual job outcomes, including failures. Text is redacted for internal paths, private cluster addresses, IAM ARNs and runner IDs; screenshot redaction is identified where used. Browser traces and secrets are never copied into Git. Artifacts also appear on each run (30-day retention; image archives one day). Download artifacts before expiry if not yet copied into the durable evidence branch.

## Required remaining capture checklist

| Required evidence | How to capture honestly | Current blocker/status |
|---|---|---|
| Running desktop/mobile frontend | Actual screenshots on [evidence/800b7b7](https://github.com/not-so-shubh/devops-project/tree/evidence/800b7b72c86042474e2245c529ecf798d7267d0b/docs/evidence); [successful browser output](evidence/compose-browser-success.txt) | Four scenarios passed; Ingress proof tracked separately |
| Passing pytest terminal screenshot | Run `pytest -v` or screenshot the successful quality job; genuine text already saved | Optional screenshot still needs capture |
| Git history screenshot | [github-commit-history.jpg](evidence/github-commit-history.jpg), captured from real public main history (earlier checkpoint) | More than ten real descriptive commits; current history linked above |
| Healthy Compose terminal screenshot | Show `docker compose ps` and actual startup output, then localhost:3000 | Stack output exists in CI; screenshot pending |
| Green Actions and GHCR SHA packages | Open final successful run and both package versions | Both SHA images published in run 39000262612; final complete pipeline pending |
| Trivy output | Both real JSON reports plus job output; explain actual clean/findings result | Both Alpine images passed HIGH/CRITICAL gate in run 39000262612; earlier Debian failure preserved |
| Real Terraform plan | In approved account, `terraform plan -out=stockpilot.tfplan`; screenshot non-empty proposed resources | AWS credentials/account and cost review needed; mock test is not this evidence |
| AWS VPC and EKS | Console region ap-south-1; show VPC/subnets and EKS with managed nodes; redact account identifiers | Explicit paid-resource approval and credentials required |
| Kubernetes Pods/Services/Helm/Ingress | Actual cluster commands and browser through Traefik, captured by CI for kind | CI kind pending; EKS separately requires AWS |
| Metrics / target UP / live Grafana | curl metrics, verify-monitoring.py, Targets page and provisioned populated dashboard | Live kind monitoring pending |
| Successful Terraform destroy | After demo and cleanup approval, remove LB/PVCs, destroy, verify state and residual AWS resources | No AWS resources have been provisioned; cannot claim destroy |
| Final live demo or recording | Follow DEMO.md, including real commit→green pipeline→deployment update | Student presentation and configured deployment required |

## Submission package

Submit https://github.com/not-so-shubh/devops-project, the exact final SHA, this index, the rubric audit, durable evidence branch/run link, and your live/recorded demonstration. Preserve originals privately where redactions are needed. Never fabricate cloud consoles, scan results, target health, populated dashboards, or destroy completion.
