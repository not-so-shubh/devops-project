# Reviewed GitOps promotion with Flux

This is an optional pull-based deployment mode, in addition to the rubric's direct Actions Helm deployment. Do not let two deployment systems own one release: disable `AWS_DEPLOY_ENABLED` before enabling Flux for that cluster.

1. Install Flux controllers with the official Flux CLI: `flux check --pre && flux install` (requires cluster-admin, not AWS infrastructure creation).
2. Bootstrap namespace, database Secret, image access, ingress, metrics-server and monitoring as documented in `docs/DEPLOYMENT.md`.
3. Apply `kubectl apply -f gitops/source.yaml`. Flux watches `main` and reconciles `gitops/apps`.
4. Select a **successfully scanned and published** commit SHA. Verify both GHCR manifests exist. Change both tags in `gitops/apps/release.yaml`, set `suspend: false`, and review/merge that change through a PR. The checked-in initial SHA is a suspended configuration, not a claim that its images passed scanning or were published.
5. Run `flux reconcile source git stockpilot && flux reconcile kustomization stockpilot`; inspect `flux get helmreleases -A`, `kubectl rollout status deployment/stockpilot-backend -n stockpilot`, ingress and real HTTP operations.
6. Roll back by reverting the promotion commit and reconciling. Flux restores desired state on its polling interval; it does not build or scan images.

The repository is the reviewable desired-state source. Git history records promotions and reversions. Secrets remain externally supplied. This configuration is not yet a verified Flux deployment; capture actual reconciliation evidence before marking the homework GitOps demonstration complete.

References: https://fluxcd.io/flux/guides/helmreleases/ and https://fluxcd.io/flux/components/kustomize/kustomizations/ .

## Disposable integration verification

CI installs checksum-verified Flux 2.9.6 controllers after the direct Helm/browser demonstration. `scripts/verify-gitops.py` creates a Git source pinned to the tested commit and a Flux Kustomization for committed `gitops/ci/`. Flux pulls those manifests, substitutes the scanned SHA, and takes ownership of the existing release. The CI overlay changes `APP_ENV` to `gitops-ci`; a ConfigMap checksum rolls backend Pods. Verification requires the fetched Git revision, Ready HelmRelease, exact image tag, and the running Pod's new environment. A final HTTP smoke checks the reconciled app. `gitops-ci.json` is written only after these assertions succeed. This overlay is confined to the ephemeral kind cluster; the separate operator workflow remains suspended until enabled deliberately.
