from concurrent.futures import ThreadPoolExecutor

import pytest
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.db import get_db
from app.main import app
from app.models import Product, StockMovement


def adjust(client, product, delta, reason="Supplier delivery"):
    return client.post(
        "/api/inventory/adjustments",
        json={"product_id": product["id"], "quantity_change": delta, "reason": reason},
    )


def test_root_and_docs(client):
    assert client.get("/").json()["service"] == "StockPilot API"
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").json()["info"]["version"] == "1.0.0"


def test_liveness(client):
    assert client.get("/health").json() == {"status": "UP"}


def test_readiness_with_database(client):
    assert client.get("/ready").json() == {"status": "READY"}


def test_database_failure_is_sanitized_and_liveness_independent(client):
    class FailedSession:
        def execute(self, *_args, **_kwargs):
            raise OperationalError("private-db-host", {}, Exception("supersecret"))

    app.dependency_overrides[get_db] = lambda: FailedSession()
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"detail": "Database temporarily unavailable"}
    assert "supersecret" not in response.text
    assert client.get("/health").status_code == 200


def test_metrics_are_prometheus_and_use_templated_routes(client):
    client.get("/api/products/98765")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert 'route="/api/products/{product_id}"' in response.text
    assert "stockpilot_http_request_duration_seconds_bucket" in response.text
    assert 'route="/api/products/98765"' not in response.text


def test_create_product_and_opening_movement(client, payload):
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["selling_price"] == "150.25"
    assert response.json()["created_at"]
    ledger = client.get("/api/inventory/movements").json()
    assert len(ledger) == 1 and ledger[0]["quantity_change"] == 12
    assert ledger[0]["reason"] == "Opening balance"


def test_zero_opening_stock_does_not_add_empty_movement(client, payload):
    payload["stock_quantity"] = 0
    assert client.post("/api/products", json=payload).status_code == 201
    assert client.get("/api/inventory/movements").json() == []


def test_sku_is_normalized_and_unique(client, payload):
    payload["sku"] = " test-001 "
    assert client.post("/api/products", json=payload).json()["sku"] == "TEST-001"
    assert client.post("/api/products", json=payload).status_code == 409
    assert len(client.get("/api/products").json()) == 1


def test_list_search_filter_and_pagination(client, product, payload):
    payload.update(sku="LOW-2", name="Low bottle", category="Lifestyle", stock_quantity=2)
    client.post("/api/products", json=payload)
    assert len(client.get("/api/products").json()) == 2
    assert len(client.get("/api/products?search=desk").json()) == 1
    assert len(client.get("/api/products?status=healthy").json()) == 1
    assert len(client.get("/api/products?status=low").json()) == 1
    assert len(client.get("/api/products?category=Lifestyle").json()) == 1
    assert len(client.get("/api/products?offset=1&limit=1").json()) == 1
    assert client.get("/api/products?limit=0").status_code == 422


def test_retrieve_product(client, product):
    assert client.get(f"/api/products/{product['id']}").json() == product


def test_update_details_preserves_balance(client, product, payload):
    payload.pop("stock_quantity")
    payload.update(name="Updated lamp", selling_price="175.00")
    response = client.put(f"/api/products/{product['id']}", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated lamp"
    assert response.json()["stock_quantity"] == 12
    assert response.json()["updated_at"] >= product["updated_at"]


def test_update_cannot_bypass_stock_ledger(client, product, payload):
    assert client.put(f"/api/products/{product['id']}", json=payload).status_code == 422


def test_update_duplicate_sku_rolls_back(client, product, payload):
    payload["sku"] = "OTHER"
    other = client.post("/api/products", json=payload).json()
    payload.pop("stock_quantity")
    payload["sku"] = product["sku"]
    assert client.put(f"/api/products/{other['id']}", json=payload).status_code == 409
    assert client.get(f"/api/products/{other['id']}").json()["sku"] == "OTHER"


def test_delete_retains_movement_audit(client, product):
    response = client.delete(f"/api/products/{product['id']}")
    assert response.status_code == 204 and response.content == b""
    assert client.get(f"/api/products/{product['id']}").status_code == 404
    ledger = client.get("/api/inventory/movements").json()
    assert ledger[0]["sku"] == product["sku"] and ledger[0]["product_id"] is None


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_product(client, method, payload):
    payload.pop("stock_quantity")
    options = {"json": payload} if method == "put" else {}
    assert getattr(client, method)("/api/products/999999", **options).status_code == 404


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", " "),
        ("sku", "bad sku"),
        ("selling_price", "-1"),
        ("selling_price", "1.123"),
        ("stock_quantity", -1),
        ("stock_quantity", 1.2),
        ("stock_quantity", True),
        ("reorder_threshold", -1),
        ("category", "x"),
        ("unknown", "oops"),
    ],
)
def test_invalid_product(client, payload, field, value):
    payload[field] = value
    assert client.post("/api/products", json=payload).status_code == 422
    assert client.get("/api/products").json() == []


def test_increment_and_decrement(client, product):
    incoming = adjust(client, product, 8)
    assert incoming.status_code == 201 and incoming.json()["quantity_after"] == 20
    outgoing = adjust(client, product, -5, "Order fulfilled")
    assert outgoing.status_code == 201 and outgoing.json()["quantity_after"] == 15
    assert client.get(f"/api/products/{product['id']}").json()["stock_quantity"] == 15


def test_insufficient_stock_atomic_rejection(client, product):
    assert adjust(client, product, -13).status_code == 409
    assert client.get(f"/api/products/{product['id']}").json()["stock_quantity"] == 12
    assert len(client.get("/api/inventory/movements").json()) == 1


def test_stock_upper_bound(client, product):
    assert adjust(client, product, 1000000).status_code == 409
    assert len(client.get("/api/inventory/movements").json()) == 1


def test_missing_adjustment_product(client):
    assert adjust(client, {"id": 999999}, 1).status_code == 404


@pytest.mark.parametrize("delta", [0, 1.5, True, "5", 1000001])
def test_invalid_adjustment(client, product, delta):
    assert adjust(client, product, delta).status_code == 422


def test_statistics_and_real_movement_trend(client, product):
    adjust(client, product, -10, "Order fulfilled")
    stats = client.get("/api/inventory/stats").json()
    assert stats["total_products"] == 1
    assert stats["total_units"] == 2
    assert float(stats["inventory_value"]) == 300.50
    assert stats["low_stock_count"] == 1 and stats["out_of_stock_count"] == 0
    assert stats["inbound_units"] == 12 and stats["outbound_units"] == 10
    assert len(stats["movement_trend"]) == 7
    assert stats["categories"] == [{"name": "Workspace", "units": 2}]


def test_empty_stats(client):
    stats = client.get("/api/inventory/stats").json()
    assert stats["total_units"] == 0 and float(stats["inventory_value"]) == 0
    assert stats["categories"] == []


def test_movement_filter_and_pagination(client, product):
    adjust(client, product, 3)
    movements = client.get(f"/api/inventory/movements?product_id={product['id']}&limit=1").json()
    assert len(movements) == 1 and movements[0]["quantity_change"] == 3
    older = client.get("/api/inventory/movements?offset=1&limit=1").json()
    assert older[0]["reason"] == "Opening balance"
    assert client.get("/api/inventory/movements?product_id=999999").json() == []


def test_data_persisted_in_independent_session(client, product, engine):
    adjust(client, product, 4)
    with Session(engine) as independent:
        assert independent.get(Product, product["id"]).stock_quantity == 16
        assert len(independent.scalars(select(StockMovement)).all()) == 2


def test_zero_balance_out_filter(client, product):
    assert adjust(client, product, -12).status_code == 201
    assert len(client.get("/api/products?status=out").json()) == 1
    assert client.get("/api/products?status=low").json() == []
    assert client.get("/api/inventory/stats").json()["out_of_stock_count"] == 1


@pytest.mark.postgres
def test_concurrent_removals_never_oversell(client, product, engine):
    if engine.dialect.name != "postgresql":
        pytest.skip("Row concurrency is verified by the PostgreSQL CI service")
    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = sorted(pool.map(lambda _: adjust(client, product, -8).status_code, range(2)))
    assert statuses == [201, 409]
    assert client.get(f"/api/products/{product['id']}").json()["stock_quantity"] == 4


def test_seed_is_explicit_and_idempotent(client, engine, monkeypatch):
    from sqlalchemy.orm import sessionmaker

    from app import seed

    monkeypatch.setattr(seed, "SessionLocal", sessionmaker(engine, expire_on_commit=False))
    assert seed.seed() == 8
    assert seed.seed() == 0
    assert len(client.get("/api/products").json()) == 8
    assert len(client.get("/api/inventory/movements").json()) == 7
