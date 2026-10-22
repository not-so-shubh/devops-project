# Demonstration guide

[Documentation hub](README.md) · [PowerPoint](presentation/README.md) · [Timed script](FINAL-DEMO-SCRIPT.md) · [Recording chapters](demo/README.md)

The personal presentation should explain the product and prove the delivery chain. The deck is ready; **no actual recording was supplied**. Personal explanation/demo assessment remains outstanding.

## Choose a truthful runtime

| Show live | Show as historical evidence |
|---|---|
| An available local Compose or local/CI kind environment | Real Sydney EKS provisioning, deployment and monitoring captured on 18 October |
| A genuine new source commit and its corresponding CI/deployment result | Approved AWS deletion completed on 22 October |

The EKS environment is deleted. The optional Actions AWS job stayed disabled by account OIDC policy. Do not present a manual Helm command or kind rollout as an automatic AWS deployment.

## Product story

1. Create a unique demo SKU with six units and inspect its opening movement.
2. Edit details/price, then remove four units with a reason; show the new balance of two.
3. Attempt to remove 99 units; explain the 409 conflict, unchanged balance and lack of a false movement.
4. Delete the catalog record and show retained movement snapshots.
5. Show search/status filters, live statistics, CSV and mobile layout.

Use synthetic data. Dashboard inventory value is selling price × quantity, not accounting cost valuation.

## Engineering proof

Show the API/data model, isolated PostgreSQL tests, migrations, non-root images, blocked-then-repaired Trivy finding, exact SHA tags, Helm/ingress/HPA, live monitoring and Flux reconciliation. The [evidence index](EVIDENCE.md) links each original receipt. Prometheus application metrics and metrics-server HPA CPU inputs are different paths.

For the commit → pipeline → deployment criterion, use a real meaningful change and observe the actual source/run/revision. Pipeline waiting can exceed the speaking plan; disclose edited waits in an accepted recording rather than replacing a fresh run with an old green screenshot.

[Timed speaking plan](FINAL-DEMO-SCRIPT.md) · [Capture checklist](FINAL-PRESENTATION-CHECKLIST.md) · [Trivy explanation](TRIVY-EXPLANATION.md) · [Instructor questions](INSTRUCTOR-QA.md).
