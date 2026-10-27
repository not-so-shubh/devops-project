# Final presentation

[Documentation hub](../README.md) · [Examiner handoff](../FINAL-PROJECT-HANDOFF.md) · [Presenter script](../FINAL-DEMO-SCRIPT.md)

[**Download the PowerPoint**](../../demo/StockPilot_Final_Presentation.pptx?raw=true) · [Open the file page](../../demo/StockPilot_Final_Presentation.pptx) · [Full-size preview](StockPilot_Presentation_Preview.png)

![Actual PowerPoint cover preview](StockPilot_Presentation_Preview.png)

The instructor requires both media files in the root [`demo/` folder](../../demo/README.md). Both the actual PowerPoint and [supplied MP4](../../demo/StockPilot_Final_Demo.mp4?raw=true) are present there. The video has no audio track; personal explanation and instructor acceptance remain to be assessed. The existing copy in `docs/presentation/` is retained for older links, with identical bytes.

## What is included

The supplied deck has **16 editable slides with 16 speaker-note parts**. It retains the black/white layout, red accents, dot-matrix wordmark, native text/diagrams and Inter/Inter Display/PT Mono font choices.

| Slides | Topics |
|---|---|
| 1–4 | Introduction, product problem, interface illustration and inventory workflow |
| 5–7 | Architecture, API/database correctness, Compose and testing |
| 8–9 | Gated delivery, GHCR and the actual libx11 Trivy failure/fix |
| 10–13 | Historical AWS/Terraform, EKS runtime, monitoring and approved cleanup |
| 14–16 | Rubric coverage, personal walkthrough plan and questions |

The deck is a **22 October 2026 evidence snapshot** citing successful application source `8944da7` and [run 39696800574](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574). Later documentation/media commits have their own runs; slide links retain the verified snapshot rather than automatically changing to a different source.

Slide 3 is explicitly an editable interface illustration with sample figures, not screenshot evidence. Its links open the genuine historical [desktop](../evidence/eks-frontend-desktop.png) and [mobile](../evidence/eks-frontend-mobile.png) captures. Slide 5 is a component schematic: the application metrics path is **FastAPI `/metrics` → Prometheus → Grafana**; the arrow beside PostgreSQL does not establish a PostgreSQL exporter. Follow the actual scrape topology in the architecture/monitoring guides. The actual p95 query uses `histogram_quantile()` as documented in [monitoring](../../monitoring/README.md).

## Download and present

1. Use **Download the PowerPoint** above, or open the GitHub file page and choose **Download raw file**.
2. Open the downloaded `.pptx` in PowerPoint or a compatible presentation editor.
3. In PowerPoint, use **View → Notes** to rehearse and **Slide Show → Use Presenter View** to see notes while presenting.
4. Install the original [Inter / Inter Display](https://github.com/rsms/inter/releases/tag/v4.1) and [PT Mono](https://fonts.google.com/specimen/PT+Mono) fonts for matching typography. Fonts are not embedded in the supplied deck.

The PNG is a render of the actual first slide, not an independently designed mockup. The package was opened/rendered through LibreOffice and imported by the presentation tooling; this is not a claim of native Microsoft PowerPoint testing.

## Preservation

The source attachment contained 15 unused slide-master content-type declarations. Only those stale package declarations were removed to clear structural validation. Every slide XML part, speaker-note part, relationship, theme and other package payload remains identical to the supplied source.

| File | SHA-256 |
|---|---|
| Supplied attachment | `dc71a92be3f6a603ca3b21d5cb0c7cccf88e8a4fd6c8663e5cd780be89fe0a84` |
| Published PowerPoint | `99f1b393a6cef1ec7c7b71746d5ad5abdac15336a499982588f533d3bc1883c5` |

The real EKS environment is deleted. Use archived AWS proof accurately and an available local/CI environment for live actions. Adding slides does not establish a completed personal demo. [Recording guide](../demo/README.md) · [Student assessment actions](../SUBMISSION.md).
