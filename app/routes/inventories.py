from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from app.models import Product, Inventory
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from typing import Optional

router = APIRouter()

LOW_STOCK_THRESHOLD = 10


@router.get("/inventory/")
async def get_inventory_status(low_stock_alert: bool = False, db: Session = Depends(get_db)):
    inventories = db.query(Inventory, Product.name).join(Product).all()

    if not inventories:
        return JSONResponse(content={"error": "No inventory records found."}, status_code=404)

    results = [{"product_name": item[1], "quantity": item[0].quantity} for item in inventories]

    if low_stock_alert:
        results = [item for item in results if item["quantity"] <= LOW_STOCK_THRESHOLD]

    return results


@router.put("/inventory/{product_id}")
async def update_inventory(
        product_id: int = None,
        quantity: Optional[int] = Body(None, embed=True),
        db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return JSONResponse(content={"error": f'Product with id {product_id} not found'})

    if not quantity:
        return JSONResponse(content={"error": "Quantity is not passed"})

    new_inventory = Inventory(product_id=product_id, quantity=quantity, created_at=datetime.now())
    db.add(new_inventory)
    db.commit()

    return {"message": f"Inventory for product {product.name} updated to {quantity}."}


@router.get("/inventory/track/{product_id}")
async def track_inventory_changes(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return JSONResponse(content={"error": f'Product with id {product_id} not found'})

    inventory_changes = db.query(Inventory).filter(Inventory.product_id == product_id).order_by(
        Inventory.created_at.desc()).all()

    results = [{"date": item.created_at, "quantity": item.quantity} for item in inventory_changes]

    return results
