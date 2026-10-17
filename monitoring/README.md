# StockPilot monitoring

Install kube-prometheus-stack 92.10.1 with `prometheus-values.yaml`, then provision `stockpilot-dashboard.json` using a ConfigMap labeled `grafana_dashboard=1` in namespace `monitoring`. The database Secret and Grafana admin Secret must be supplied externally; see docs/DEPLOYMENT.md.

The ServiceMonitor selects the backend Service's name, instance and component labels, in the application's namespace. Prometheus discovers ServiceMonitors in the namespace labeled `kubernetes.io/metadata.name=stockpilot` and requires `release=monitoring`. Its port name is `http`, matching the backend Service on 8000.

Dashboard queries use actual `stockpilot_http_requests_total` and `stockpilot_http_request_duration_seconds_bucket` metrics. Route labels use route templates, avoiding unbounded product-ID cardinality. The server-error ratio includes only HTTP 5xx. Generate traffic with `scripts/load-test.sh`; wait for at least two 15-second scrapes and query Prometheus before capturing the dashboard.

A clean scan or an empty graph is not proof of security or successful monitoring. Live target and panel evidence is tracked in docs/EVIDENCE.md. This lightweight monitoring uses ephemeral storage; use persistent retention and backups before operating a real business.
