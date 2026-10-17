# Reviewed GitOps promotion with Flux

This is an optional pull-based deployment mode, in addition to the rubric's direct Actions Helm deployment. Do not let two deployment systems own one release: disable `AWS_DEPLOY_ENABLED` before enabling Flux for that cluster.

1. Install Flux controllers with the official Flux CLI: `flux check --pre && flux install` (requires cluster-admin, not AWS infrastructure creation).
2. Bootstrap namespace, database Secret, image access, ingress, metrics-server and monitoring as documented in `docs/DEPLOYMENT.md`.
3. Apply `kubectl apply -f gitops/source.yaml`. Flux watches `main` and reconciles `gitops/apps`.
4. Select a **successfully scanned and published** commit SHA. Verify both GHCR manifests exist. Change both tags in `gitops/apps/release.yaml`, set `suspend: false`, and review/merge that change through a PR. The checked-in SHA `9462f34dc3c8f6321af23a85d11296d980839595` passed both image scans and public GHCR publication in [run 39045365598](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598); the operator release stays suspended until cluster bootstrap is complete.
5. Run `flux reconcile source git stockpilot && flux reconcile kustomization stockpilot`; inspect `flux get helmreleases -A`, `kubectl rollout status deployment/stockpilot-backend -n stockpilot`, ingress and real HTTP operations.
6. Roll back by reverting the promotion commit and reconciling. Flux restores desired state on its polling interval; it does not build or scan images.

The repository is the reviewable desired-state source. Git history records promotions and reversions. Secrets remain externally supplied. The disposable integration mode has been verified in the [complete successful run](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598); [the original record](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/gitops-ci.json) shows Flux fetched the tested Git revision and completed Helm revision 2 with APP_ENV=gitops-ci. The separate operator/EKS release remains suspended and is not claimed as deployed.

References: https://fluxcd.io/flux/guides/helmreleases/ and https://fluxcd.io/flux/components/kustomize/kustomizations/ .

## Disposable integration verification

CI installs checksum-verified Flux 2.9.6 controllers after the direct Helm/browser demonstration. `scripts/verify-gitops.py` creates a Git source pinned to the tested commit and a Flux Kustomization for committed `gitops/ci/`. Flux pulls those manifests, substitutes the scanned SHA, and takes ownership of the existing release. The CI overlay changes `APP_ENV` to `gitops-ci`; a ConfigMap checksum rolls backend Pods. Verification requires the fetched Git revision, Ready HelmRelease, exact image tag, and the running Pod's new environment. A final HTTP smoke checks the reconciled app. `gitops-ci.json` is written only after these assertions succeed. This overlay is confined to the ephemeral kind cluster; the separate operator workflow remains suspended until enabled deliberately.

Pull-request jobs consistently check out, test, build, scan and deploy the actual PR head `SOURCE_SHA`. Flux clones the source branch pinned to that same reachable commit, and the fetched artifact must match it. A synthetic merge-ref clone failed with an object-not-found error in run 39051158786; that failed run is not counted as green evidence. Main pushes still use the real main commit and run a separate complete gate before publication. Source reconciliation failures preserve describe/condition diagnostics in `gitops-diagnostics-ci.txt`. See [Flux branch plus commit pinning](https://fluxcd.io/flux/components/source/gitrepositories/#commit-example).
