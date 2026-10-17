import time
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import func, or_, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .db import get_db
from .models import Product, StockMovement
from .schemas import MovementOut, ProductCreate, ProductDetails, ProductOut

app = FastAPI(title="StockPilot API", version="1.0.0", description="Inventory operations and stock ledger")
DB = Annotated[Session, Depends(get_db)]
REQUESTS = Counter("stockpilot_http_requests_total", "HTTP requests", ["method", "route", "status"])
LATENCY = Histogram("stockpilot_http_request_duration_seconds", "HTTP latency", ["method", "route"])


@app.middleware("http")
async def measure_http(request: Request, call_next):
    start = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = getattr(request.scope.get("route"), "path", "unmatched")
        if request.url.path != "/metrics":
            REQUESTS.labels(request.method, route, str(status)).inc()
            LATENCY.labels(request.method, route).observe(time.perf_counter() - start)


@app.exception_handler(SQLAlchemyError)
async def database_error(_request: Request, _exc: SQLAlchemyError):
    return JSONResponse(status_code=503, content={"detail": "Database temporarily unavailable"})


def commit(db):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "SKU already exists or inventory constraint violated") from None


def product_or_404(db, product_id):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(404, "Product not found")
    return product


@app.get("/")
def root():
    return {"service": "StockPilot API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/ready")
def ready(db: DB):
    db.execute(text("SELECT 1"))
    # Also reject an unmigrated database: connectivity alone is insufficient.
    db.execute(select(Product.id).limit(1))
    return {"status": "READY"}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/products", response_model=list[ProductOut])
def list_products(
    db: DB,
    search: str = Query(default="", max_length=160),
    status: Literal["all", "healthy", "low", "out"] = "all",
    category: str = Query(default="", max_length=80),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    query = select(Product)
    if search:
        term = f"%{search.strip()}%"
        query = query.where(or_(Product.name.ilike(term), Product.sku.ilike(term)))
    if category:
        query = query.where(Product.category == category)
    if status == "low":
        query = query.where(Product.stock_quantity <= Product.reorder_threshold, Product.stock_quantity > 0)
    elif status == "out":
        query = query.where(Product.stock_quantity == 0)
    elif status == "healthy":
        query = query.where(Product.stock_quantity > Product.reorder_threshold)
    return list(db.scalars(query.order_by(Product.created_at.desc(), Product.id.desc()).offset(offset).limit(limit)))


@app.get("/api/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: DB):
    return product_or_404(db, product_id)


@app.post("/api/products", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: DB):
    product = Product(**payload.model_dump())
    db.add(product)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "SKU already exists") from None
    if product.stock_quantity:
        db.add(StockMovement(
            product_id=product.id, product_name=product.name, sku=product.sku,
            quantity_change=product.stock_quantity, quantity_after=product.stock_quantity,
            reason="Opening balance",
        ))
    commit(db)
    return product


@app.put("/api/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductDetails, db: DB):
    product = product_or_404(db, product_id)
    for key, value in payload.model_dump().items():
        setattr(product, key, value)
    commit(db)
    return product


@app.delete("/api/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: DB):
    db.delete(product_or_404(db, product_id))
    commit(db)
    return Response(status_code=204)
