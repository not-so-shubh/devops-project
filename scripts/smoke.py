"""Real HTTP smoke test against an already running stack; cleans up its product."""

import json
import os
import urllib.request
from uuid import uuid4

base = os.getenv("BASE_URL", "http://localhost:3000")


def request(path, method="GET", data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        base + path, data=body, method=method, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response) if response.status != 204 else None


product = request(
    "/api/products",
    "POST",
    {
        "sku": "SMOKE-" + uuid4().hex[:8],
        "name": "Smoke validation item",
        "category": "Verification",
        "selling_price": "10.50",
        "stock_quantity": 5,
        "reorder_threshold": 2,
    },
)
try:
    movement = request(
        "/api/inventory/adjustments",
        "POST",
        {"product_id": product["id"], "quantity_change": -2, "reason": "HTTP smoke test"},
    )
    assert movement["quantity_after"] == 3
    assert request(f"/api/products/{product['id']}")["stock_quantity"] == 3
    assert request("/api/inventory/stats")["total_products"] >= 1
    print(
        "PASS: frontend-origin API proxy, create, stock decrement, persistent retrieval and stats"
    )
finally:
    request(f"/api/products/{product['id']}", "DELETE")
    print("Cleaned up smoke product; audit history retained")
