# Final project handoff

[Repository](https://github.com/not-so-shubh/devops-project) · [Documentation hub](README.md) · [PowerPoint](presentation/README.md) · [Evidence](EVIDENCE.md)

## A short assessment route

1. Read the product overview and open the genuine [desktop](evidence/eks-frontend-desktop.png)/[mobile](evidence/eks-frontend-mobile.png) captures.
2. Download the [editable presentation](../demo/StockPilot_Final_Presentation.pptx?raw=true) and use its speaker notes.
3. Inspect [the verified application CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574), [test output](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/pytest-postgres.txt), [scan reports](EVIDENCE.md#source-pinned-ci-evidence) and [Flux receipt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/gitops-ci.json).
4. Review the separate real [AWS runtime](AWS-EKS-RUNTIME-VERIFICATION.md) and [approved cleanup](AWS-CLEANUP-VERIFICATION.md).
5. Assess the student's own explanation/demo and the exact [46-row rubric](RUBRIC-CHECKLIST.md).

## What StockPilot is

An original inventory workspace for small businesses. Users manage SKU-based products, receive/remove stock with reasons, detect low balances, export records and inspect retained movement history. Database-backed statistics include inventory value and seven-day stock flow.

React/Vite and Nginx serve the browser. FastAPI/Pydantic provide validated APIs; SQLAlchemy/Psycopg and PostgreSQL store products/movements; Alembic manages schema. Conditional SQL plus one transaction prevents overselling and phantom ledger entries. [Architecture](ARCHITECTURE.md) · [Backend](../backend/README.md) · [Frontend](../frontend/README.md).

## Run and verify

From the repository root, follow the [secure local setup](../README.md#quick-start), then:

```bash
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
docker compose exec backend python -m app.seed
python3 scripts/smoke.py
```

The app is localhost:3000 and Swagger localhost:8000/docs. Existing database credentials must match the volume. [Deployment](DEPLOYMENT.md) separates Compose, local kind and historical EKS procedures. Application code and deployment/workflow files were not changed for the documentation/media polish.

[Testing](TESTING.md) contains Python/frontend/Playwright commands and PostgreSQL isolation rules. The verified application baseline has **44 PostgreSQL passes, 97.67% coverage**, four desktop/mobile scenarios in each runtime path, migration consistency and container-restart persistence proof.

## Delivery and images

The [unchanged workflow](../.github/workflows/ci-cd.yml) gates source through quality, infrastructure, Compose, image scans, GHCR publication and disposable kind/Helm/monitoring/Flux validation. Main and PR source revisions are consistent; PRs do not publish or deploy AWS.

Baseline image tags:

```text
ghcr.io/not-so-shubh/stockpilot-backend:8944da7ddf2be0845a593c2f65482eb922e6d9f7
ghcr.io/not-so-shubh/stockpilot-frontend:8944da7ddf2be0845a593c2f65482eb922e6d9f7
```

[Backend receipt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ghcr-backend.json) and [frontend receipt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ghcr-frontend.json) confirm anonymous pull, exact source and runtime UIDs 10001/101. [Current Actions results](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml) show later documentation revisions separately.

## Presentation and recording

The [16-slide PowerPoint](presentation/README.md) preserves editable content, notes and the supplied black/white/red design. The [preview](presentation/StockPilot_Presentation_Preview.png) is rendered from its actual cover. The deck is a dated application-evidence snapshot at `8944da7`.

**Supplied demo MP4: uploaded.** Both actual media files are present in the root [`demo/` folder](../demo/README.md). The [video](../demo/StockPilot_Final_Demo.mp4?raw=true) runs 11:00.56 at 1920 × 1080 and has no audio track. Personal explanation and instructor acceptance remain to be assessed. [Planned chapters and file instructions](demo/README.md) · [Timed script](FINAL-DEMO-SCRIPT.md) · [Presenter checklist](FINAL-PRESENTATION-CHECKLIST.md).

## Real AWS lifecycle

| Phase | Verified historical execution |
|---|---|
| Plan/provision, 18 October | Real 33-resource plan; Sydney VPC, two public/two private subnets across two AZs, EKS 1.35 and managed workers |
| Runtime/capture | Two Ready `m7i-flex.large` workers, two frontend/backend replicas, Bound 5 GiB gp3 database, Helm/ingress/browser/HPA and monitoring proof |
| Backup/cleanup, 22 October | Separate deletion approval, retained PostgreSQL dump, LB/PVC removal, saved destroy-plan apply, empty state and project residual checks |

The cleanup removed 33 Terraform resources, two workers, three EBS disks, the ingress LB, VPC/NAT/EIP, project roles/log group and matching ENIs. The cluster is **deleted**, not a live demo endpoint. The actual command applied a saved `terraform plan -destroy` plan; no different literal command is claimed. [Receipt and limits](AWS-CLEANUP-VERIFICATION.md).

## Assessment and known limits

| Category | Audit coverage |
|---|---:|
| Verified technical criteria | 43 criteria / 94 points |
| Student Trivy explanation and personal demonstration | 2 criteria / 4 points, still to assess |
| Official form | 1 criterion / 2 points, excluded from this task |

These are evidence categories, not guaranteed or awarded marks. The file upload does not complete a personal presentation. Use genuine saved Console/terminal captures for exact submission formats; deleted AWS Console views cannot be recreated from JSON as authentic images.

Automatic Actions deployment to EKS remains disabled because account policy denied OIDC-provider access. The real EKS release was manual; automatic kind/Flux validation is separate. No cloud changes or new paid infrastructure were needed for this handoff. The original AWS runtime window was exceeded; actual billing totals/credits remain unverified.

The capstone uses synthetic inventory, one database, one NAT and ephemeral monitoring. Business operation needs authentication/RBAC, TLS, availability planning and tested restore/retention. [Operational tradeoffs](ARCHITECTURE.md#operational-tradeoffs).

## Student's final checklist

- [ ] Download the deck and rehearse its notes using [the instructor questions](INSTRUCTOR-QA.md).
- [ ] Personally explain one real CVE and the scan limits using [Trivy preparation](TRIVY-EXPLANATION.md).
- [ ] Perform a real commit → CI → observed deployment update in an available permitted local/CI environment.
- [x] Add the supplied recording as `demo/StockPilot_Final_Demo.mp4` alongside the deck; original bytes preserved and full-file decoding checked. No audio track is present.
- [ ] Review recording coverage and instructor acceptance; arrange any required spoken explanation.
- [ ] Retain the genuine required screenshots and private AWS/backup evidence with correct environment labels.
- [ ] Handle the official submission form yourself. **Student action — excluded from this task.**

[Project MIT license](../LICENSE) · [Originality/reference notice](../NOTICE.md) · [Retained upstream license](../LICENSE.reference).
