import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

# A disconnected default engine is fine; dependencies are always replaced below.
os.environ.setdefault("DATABASE_URL", "sqlite://")
from app.db import Base, get_db, make_engine
from app.main import app
from app.models import Product, StockMovement


@pytest.fixture()
def engine(tmp_path):
    url = os.environ.get("TEST_DATABASE_URL", f"sqlite:///{tmp_path}/stockpilot_test.db")
    parsed = make_url(url)
    if parsed.get_backend_name() != "sqlite" and not (parsed.database or "").endswith("_test"):
        pytest.fail("Refusing destructive test setup: database name must end with _test")
    db_engine = make_engine(url)
    Base.metadata.create_all(db_engine)
    with Session(db_engine) as db:
        db.query(StockMovement).delete()
        db.query(Product).delete()
        db.commit()
    yield db_engine
    db_engine.dispose()


@pytest.fixture()
def client(engine):
    def override_db():
        with Session(engine, expire_on_commit=False) as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def payload():
    return {
        "sku": "TEST-001",
        "name": "Desk lamp",
        "category": "Workspace",
        "selling_price": "150.25",
        "stock_quantity": 12,
        "reorder_threshold": 5,
        "description": "Warm task lighting",
    }


@pytest.fixture()
def product(client, payload):
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201, response.text
    return response.json()
