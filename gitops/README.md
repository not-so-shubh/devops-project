# GitOps with Flux

[Documentation hub](../docs/README.md) · [Workflow](../.github/workflows/ci-cd.yml) · [Deployment](../docs/DEPLOYMENT.md)

## What was verified

In disposable kind, the direct Helm/browser checks finish first. The CI verifier then installs Flux and deliberately transfers release ownership to the committed [`ci/`](ci/) overlay. Source-controller fetches the tested branch/commit; kustomize-controller substitutes the tested image SHA; helm-controller upgrades StockPilot. A changed ConfigMap checksum rolls backend Pods.

The actual [Flux receipt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/gitops-ci.json) for source `8944da7` records the fetched source SHA, Ready HelmRelease, **Helm revision 2** and the `gitops-ci` environment. The verifier also checks the running Pod's environment and final HTTP health. This is automatic pull reconciliation in kind, not automatic deployment to AWS.

## Release ownership

Choose one continuous owner for one release. Repeated direct `helm upgrade` from Actions while Flux reconciles the same release can cause competing desired states. The CI exercise uses a controlled handoff in a disposable cluster. A permitted future operator cluster would disable direct Actions ownership before enabling Flux.

Flux retrieves declared state; it does not build or scan images. Promotion must select successfully scanned and published source-SHA tags. Git history records promotion and rollback by revert. Secrets remain externally supplied.

## Operator overlay

[`source.yaml`](source.yaml) and [`apps/release.yaml`](apps/release.yaml) are an optional operator path. The checked-in release remains suspended and retains its own historical scanned SHA. It was not enabled against EKS. Review actual source/registry receipts, bootstrap storage/controllers/Secrets and obtain any required account/runtime approval before using a future permitted cluster.

For an already authorized cluster only, the operator sequence is: install/check Flux, bootstrap prerequisites, review the exact source and release values, choose verified image tags, unsuspend deliberately, reconcile, then inspect fetched revision, Helm conditions and running Pods. See [official HelmRelease guidance](https://fluxcd.io/flux/guides/helmreleases/).

## Source consistency and diagnostics

PR checks use the reachable PR head SHA for tests, builds, image tags and Flux fetches. A synthetic merge commit failed to clone in historical run 39051158786; that failure is retained, not counted as green evidence. Main pushes validate their actual main SHA separately. Reconciliation errors preserve describe/condition diagnostics.

Relevant implementation: [`verify-gitops.py`](../scripts/verify-gitops.py), [`ci/kustomization.yaml`](ci/kustomization.yaml) and [`ci/release.yaml`](ci/release.yaml). [Evidence manifest](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ci-run.json) · [Troubleshooting](../docs/TROUBLESHOOTING.md).
