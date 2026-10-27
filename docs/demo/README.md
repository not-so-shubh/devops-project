# Final demo recording

[Required submission media](../../demo/README.md) · [Documentation hub](../README.md) · [PowerPoint](../presentation/README.md) · [Timed script](../FINAL-DEMO-SCRIPT.md)

**Status: [supplied MP4 uploaded](../../demo/StockPilot_Final_Demo.mp4?raw=true).** Both required files are present in the root `demo/` folder. The video runs 11:00.56 at 1920 × 1080 and has no audio track. [File details and checksum](../../demo/README.md). Personal explanation and instructor acceptance remain to be assessed. This `docs/demo/` page is the chapter guide.

The presentation and this chapter plan are preparation. They do not establish completion of the student's personal explanation or live/accepted recorded demonstration.

## Recording plan

Use local Compose or an available local/CI Kubernetes environment for live product actions. The real Sydney EKS deployment and monitoring are historical, captured before approved deletion. The optional Actions AWS deployment job was skipped because of account-policy restrictions.

| Chapter | Show and explain |
|---:|---|
| 1 | Introduce StockPilot, the stock-control problem and original inventory workflow |
| 2 | Open the actual dashboard, desktop/mobile layout and database-derived statistics |
| 3 | Create, inspect, edit, search and delete a uniquely named product |
| 4 | Adjust stock, reject overselling, show retained ledger and actual PostgreSQL persistence proof |
| 5 | Inspect FastAPI Swagger, health/readiness, product and adjustment APIs |
| 6 | Explain Dockerfiles, non-root IDs, Compose services and migration ordering |
| 7 | Show real Pytest output, coverage, browser acceptance and source-specific Actions jobs |
| 8 | Explain the actual Trivy libx11 finding, blocked publication, package fix and clean follow-up reports |
| 9 | Inspect both GHCR SHA tags, public-pull receipts and source revision |
| 10 | Show Helm, Ready replicas, Services, ingress and HPA resource metrics in the chosen environment |
| 11 | Present genuine historical Sydney VPC/EKS/worker evidence with its capture date |
| 12 | Show actual Prometheus targets and Grafana panels; distinguish HPA CPU metrics |
| 13 | Present the approved saved destroy-plan execution, empty state and scoped residual checks |
| 14 | Perform a genuine meaningful commit, observe its real CI run and the corresponding deployment-update proof |

These are planned chapters, not verified timestamps or a coverage assessment of the supplied video. Aim for 10–15 minutes of speaking; a fresh pipeline can take longer. If the instructor accepts an edited recording, disclose waiting-time cuts and retain the actual commit/run/deployment continuity.

## Capture checklist

- Use synthetic inventory. Hide credentials, private AWS identifiers and password prompts.
- Capture readable terminal/browser text and usable audio.
- Label Compose, disposable kind and historical EKS accurately.
- Demonstrate personally. A prior green run or automated screenshot is not a recording of student understanding.
- Use only genuine pre-deletion AWS Console images already saved; do not fabricate replacement Console screens.
- Check the recording and its final link from another browser before sharing it.

## Supplied recording

The original [StockPilot_Final_Demo.mp4](../../demo/StockPilot_Final_Demo.mp4?raw=true) is committed beside the PowerPoint without re-encoding. [Media details](../../demo/README.md) record its size, duration, codec and checksum. Full-file decoding completed without reported errors; there is no audio stream.

Review chapter coverage and instructor acceptance separately. Add verified chapter timestamps only after reviewing the actual recording. If spoken explanation is required, arrange it separately or supply a replacement recording with audio.
