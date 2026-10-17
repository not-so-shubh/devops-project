"""Prove a committed inventory record survives actual Compose PostgreSQL restart."""

import json
import subprocess
import time
import urllib.error
import urllib.request
import uuid

base = "http://127.0.0.1:3000"


def request(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        base + path, data=body, method=method, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        payload = response.read()
        return json.loads(payload) if payload else None


sku = "PERSIST-" + uuid.uuid4().hex[:12].upper()
product = request(
    "POST",
    "/api/products",
    {
        "sku": sku,
        "name": "Persistence verification",
        "category": "Verification",
        "selling_price": "12.50",
        "stock_quantity": 7,
        "reorder_threshold": 2,
        "description": "Disposable CI restart probe",
    },
)
try:
    subprocess.run(["docker", "compose", "restart", "postgres"], check=True)
    for _ in range(60):
        try:
            restored = request("GET", f"/api/products/{product['id']}")
            break
        except (urllib.error.URLError, TimeoutError):
            time.sleep(1)
    else:
        raise SystemExit("PostgreSQL/API did not recover within 60 seconds")
    assert restored["sku"] == sku and restored["stock_quantity"] == 7
    movements = request("GET", f"/api/inventory/movements?product_id={product['id']}")
    assert any(item["quantity_after"] == 7 for item in movements)
    print(
        "PASS: product balance and stock ledger survived PostgreSQL container restart; API pool reconnected"
    )
finally:
    request("DELETE", f"/api/products/{product['id']}")
