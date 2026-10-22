# Final presentation checklist

[Documentation hub](README.md) · [PowerPoint](presentation/README.md) · [Timed script](FINAL-DEMO-SCRIPT.md) · [Submission status](SUBMISSION.md)

## Prepared

- [x] Editable 16-slide PowerPoint and actual cover preview available, with speaker notes preserved.
- [x] Verified application baseline: tests, image gates, GHCR, kind/Helm/monitoring and Flux.
- [x] Real historical EKS provisioning/runtime captured separately from kind evidence.
- [x] Separate cleanup approval, retained database backup, saved destroy-plan apply and project residual checks completed.
- [x] Official form left for the student.

## Student preparation

- [ ] Open the downloaded deck, check fonts/display and rehearse its notes.
- [ ] Start an available permitted local/CI runtime; confirm product actions and microphone/terminal readability.
- [ ] Explain the actual Trivy finding and scan limits in your own words.
- [ ] Perform and observe a genuine commit → CI → deployment-update chain.
- [ ] Supply a real recording if required. **No video was provided for this handoff.**
- [ ] Check the final shared video link and audio from another browser.

## Required proof formats

| Item | Check |
|---|---|
| App desktop/mobile | Real running-app captures, with environment/date labels |
| Tests/Compose/security | Readable original output from the cited run; exact source SHA |
| Git/GHCR | Actual commit history and both source-SHA package tags |
| Terraform | Genuine plan and completed saved destroy-plan output |
| AWS Console | Genuine pre-deletion Sydney VPC/EKS screenshots already saved |
| Kubernetes | Actual Pods, Services, Helm list and ingress/browser output |
| Observability | Actual `/metrics`, UP targets and populated Grafana panels |
| Personal demo | Student understanding plus observed source/run/deployment continuity |

The deleted EKS environment cannot be reconstructed as authentic Console images from CLI archives. Existing technical proof does not certify every exact screenshot format. Keep raw AWS identifiers, credentials, state and database contents private.

## Final boundary

The audit remains **94 verified technical points, 4 personal-assessment points and 2 excluded form points**, not awarded marks. A deck upload or recording guide does not complete M6.3/M10.2. AWS Actions deployment remains disabled by account policy. No cloud recreation or resource change is part of this handoff.
