# Monitoring and autoscaling

[Documentation hub](../docs/README.md) · [Deployment](../docs/DEPLOYMENT.md#monitoring-and-cleanup) · [Evidence](../docs/EVIDENCE.md)

## Two metric paths

| System | Input and purpose |
|---|---|
| Prometheus / Grafana | Application HTTP counters and latency histograms for observation |
| metrics-server / HPA | Kubernetes CPU resource metrics for backend replica decisions |

The backend exports `/metrics`. Route-template labels avoid unbounded per-product labels, and requests to `/metrics` do not inflate application request counters. HPA does not consume the Grafana application dashboard.

## Configuration and discovery

[`prometheus-values.yaml`](prometheus-values.yaml) configures the lightweight kube-prometheus-stack 92.10.1 demo. [`stockpilot-dashboard.json`](stockpilot-dashboard.json) provides four panels. Its ConfigMap carries `grafana_dashboard=1` in namespace `monitoring`; Grafana credentials come from an external Secret.

The [ServiceMonitor](../helm/stockpilot/templates/servicemonitor.yaml) selects the backend Service's application instance/component labels and named `http` port. Prometheus discovery expects the application namespace label and `release=monitoring`. The namespace must exist before monitoring bootstrap.

| Panel | Actual expression |
|---|---|
| Request rate | `sum(rate(stockpilot_http_requests_total{namespace="stockpilot"}[2m]))` |
| p95 latency | `histogram_quantile(0.95, sum by (le) (rate(stockpilot_http_request_duration_seconds_bucket{namespace="stockpilot"}[2m])))` |
| Server-error ratio | 5xx request rate divided by total rate, with a zero fallback and nonzero denominator clamp |
| Backend targets | `sum(up{namespace="stockpilot",service="backend"})` |

The ratio panel uses `percentunit` with maximum 1, displayed as **0–100%**. That completed real EKS display correction changed the axis, not metric values.

## Verify an available local/CI cluster

Use separate terminals for the Prometheus and Grafana port-forwards in [Deployment](../docs/DEPLOYMENT.md#local-kind). Open localhost:9090/targets and localhost:3001. Generate traffic against the correct app origin:

```bash
BASE_URL=http://localhost:3000 REQUESTS=60 bash scripts/load-test.sh
python3 scripts/verify-monitoring.py
```

The verifier needs the localhost:9090 port-forward and asserts an UP StockPilot target plus a positive request-rate query. Allow at least two scrape intervals before inspection. A zero error ratio can be correct; an empty traffic panel is not a successful live-data check.

On the historical EKS capture, two targets were UP, the refreshed sampled request rate was **2.1333333333333333 requests/second**, and authenticated Grafana had four populated panels. [Exact capture provenance](../docs/AWS-EKS-CAPTURE-REVIEW.md). HPA CPU metrics were available at low load; no load-induced scale-out was claimed.

Monitoring storage is ephemeral in the capstone preset. Business use needs retention, backups and access controls; keep monitoring port-forwards private. [Current application baseline's original query](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/prometheus-query.json) · [Kind Grafana capture](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/grafana-dashboard.png).
