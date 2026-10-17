# Architecture and decisions

StockPilot is a single-workspace inventory platform. The browser reads all displayed data from the API. Database-backed seed examples are optional. Inventory, stock history, and aggregate statistics share one relational source of truth.

```mermaid
erDiagram
  PRODUCTS o|--o{ STOCK_MOVEMENTS : retains
  PRODUCTS {
    int id PK
    string sku UK
    string name
    string category
    decimal selling_price
    int stock_quantity
    int reorder_threshold
    string description
    timestamp created_at
    timestamp updated_at
  }
  STOCK_MOVEMENTS {
    int id PK
    int product_id FK
    string product_name
    string sku
    int quantity_change
    int quantity_after
    string reason
    timestamp created_at
  }
```

The nullable foreign key uses `ON DELETE SET NULL`. Movement snapshots keep their original SKU/name after edits or deletion. Quantities are integers; prices use `NUMERIC(12,2)` and Decimal validation, not floating-point storage. Responses normalize timestamps to UTC, including local SQLite tests.

An adjustment executes `UPDATE products SET stock_quantity = stock_quantity + delta WHERE id = ... AND stock_quantity + delta BETWEEN 0 AND 1000000 RETURNING ...`, then inserts the movement and commits. PostgreSQL serializes competing writes to the row and reevaluates the condition. An insufficient balance returns 409 without a movement. A failure before commit rolls back both operations. Product creation similarly commits its opening balance with the product.

The API imports models but never creates tables on startup. Alembic is the production schema owner. Readiness runs a real query and checks the products table; liveness stays independent of a database outage. The migration service/Job is the sole migration runner for a deployment. Release migrations must be backward compatible during rolling updates. Database recovery requires tested backups; Helm rollback alone is insufficient.

The frontend keeps URLs relative, avoiding build-time cluster hostnames. Nginx uses 8080 as UID 101 and proxies `/api/` unchanged to Service `backend:8000`; Ingress handles `/api` directly, then `/` to frontend. The chart intentionally supports one StockPilot release per namespace because these Service DNS names are stable. Use separate namespaces for dev/prod or additional instances.

Kubernetes runs two frontend replicas and a backend HPA with minimum two and maximum six at 65% of the 100m CPU request. Limits protect the node; requests make scheduling and CPU utilization meaningful. Metrics-server supplies resource metrics for HPA. Prometheus is a separate metrics system for observation, not the HPA CPU data provider.

The demonstration PostgreSQL StatefulSet has a PVC. EKS uses encrypted gp3 via the EBS CSI driver, with Pod Identity granting only the CSI role EBS permissions. The CSI role, EKS roles and access entries are defined in Terraform. CNI permissions are attached to the demo node role; a production hardening step is a dedicated CNI Pod Identity/IRSA role. Single NAT and a single DB are documented availability tradeoffs.

HTTP counters and latency histograms use route-template labels, including status codes, and exclude `/metrics` requests. The Grafana dashboard aggregates all backend replicas. ServiceMonitor selection is explicit on namespace, release label and Service labels/port. Its namespace label must exist before monitoring installation.

The CI path is reproducible and gated: quality → Compose → build/scan → publish and kind integration → optional EKS. Candidate image tar archives ensure the pushed bytes are the scanned bytes. AWS OIDC trusts the exact repository's `production` environment. IAM permits describing only the intended EKS cluster; EKS access grants edit only in `stockpilot`, while a human operator bootstraps namespace, storage, monitoring and secrets.
