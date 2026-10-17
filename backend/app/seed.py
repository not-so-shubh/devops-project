"""Explicit, repeatable demo seed. Run after `alembic upgrade head`."""

from decimal import Decimal

from sqlalchemy import select

from .db import SessionLocal
from .models import Product, StockMovement

SAMPLES = [
    (
        "DSK-001",
        "Arc desk lamp",
        "Workspace",
        "2499.00",
        42,
        10,
        "Adjustable aluminum task light, warm white.",
    ),
    (
        "AUD-002",
        "Studio headphones",
        "Electronics",
        "5999.00",
        28,
        8,
        "Over-ear wireless headphones with soft ear cushions.",
    ),
    (
        "BAG-003",
        "Everyday tote",
        "Accessories",
        "1299.00",
        7,
        15,
        "Heavyweight recycled cotton, charcoal.",
    ),
    (
        "BOT-004",
        "Insulated bottle",
        "Lifestyle",
        "899.00",
        64,
        20,
        "750 ml stainless steel bottle, sage.",
    ),
    (
        "KEY-005",
        "Mechanical keyboard",
        "Electronics",
        "7499.00",
        5,
        10,
        "Compact 75% keyboard with tactile switches.",
    ),
    (
        "NTB-006",
        "Grid notebook set",
        "Workspace",
        "549.00",
        96,
        25,
        "Three lay-flat notebooks, recycled paper.",
    ),
    (
        "HUB-007",
        "USB-C travel hub",
        "Electronics",
        "3299.00",
        0,
        12,
        "Six ports in a compact aluminum housing.",
    ),
    (
        "PLN-008",
        "Weekly desk planner",
        "Workspace",
        "699.00",
        33,
        10,
        "Undated planner with a minimal weekly layout.",
    ),
]


def seed():
    with SessionLocal() as db:
        added = 0
        for sku, name, category, price, quantity, threshold, description in SAMPLES:
            if db.scalar(select(Product.id).where(Product.sku == sku)) is not None:
                continue
            product = Product(
                sku=sku,
                name=name,
                category=category,
                selling_price=Decimal(price),
                stock_quantity=quantity,
                reorder_threshold=threshold,
                description=description,
            )
            db.add(product)
            db.flush()
            if quantity:
                db.add(
                    StockMovement(
                        product_id=product.id,
                        product_name=name,
                        sku=sku,
                        quantity_change=quantity,
                        quantity_after=quantity,
                        reason="Opening balance",
                    )
                )
            added += 1
        db.commit()
        return added


if __name__ == "__main__":
    print(f"Seeded {seed()} new products (existing SKUs preserved).")
