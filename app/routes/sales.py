from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from app.models import Sale, Product, Category
from app.db import get_db
from typing import Optional

router = APIRouter()


@router.get("/sales")
async def get_sales(
        start_date: date = None,
        end_date: date = None,
        product_id: int = None,
        category: str = None,
        db: Session = Depends(get_db)
):
    if not start_date or not end_date or not product_id or not category:
        return JSONResponse(content={"error": "start_date end_date product_id  category_name must be provided"},
                            status_code=400)

    query = db.query(Sale).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    if product_id:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return JSONResponse(content={"error": "Product doesn't exist"})
        query = query.filter(Sale.product_id == product_id)

    if category:
        category_exists = db.query(Category).filter(Category.name == category).first()
        if not category_exists:
            return JSONResponse(content={"error": "category doesn't exist"})
        query = query.join(Product).join(Category).filter(Category.name == category)

    sales_data = query.all()
    return {"sales_data": sales_data}


@router.get("/revenue/daily")
async def get_daily_revenue(
        start_date: date = None,
        end_date: date = None,
        db: Session = Depends(get_db)
):
    if not start_date or not end_date:
        return JSONResponse(content={"error": "start_date and end_date must be provided"}, status_code=400)

    result = (
        db.query(func.date(Sale.sale_date), func.sum(Sale.sale_price))
        .filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
        .group_by(func.date(Sale.sale_date))
    )
    daily_revenue = result.all()
    converted_data = [{"date": date.isoformat(), "revenue": revenue} for date, revenue in daily_revenue]
    return {"daily_revenue": converted_data}


@router.get("/revenue/comparison")
async def compare_revenue(
        start_date_1: date = None,
        end_date_1: date = None,
        start_date_2: date = None,
        end_date_2: date = None,
        category: Optional[str] = None,
        db: Session = Depends(get_db)
):
    if not start_date_1 or not end_date_1 or not start_date_2 or not end_date_2:
        return JSONResponse(
            content={"error": "start_date and end_date must be provided for both dates to compare the revenue"})

    base_query = db.query(Category.name, func.sum(Sale.sale_price * Sale.sale_quantity)).join(Sale.product).join(
        Product.category)
    query_1 = base_query.filter(Sale.sale_date >= start_date_1, Sale.sale_date <= end_date_1)

    query_2 = base_query.filter(Sale.sale_date >= start_date_2, Sale.sale_date <= end_date_2)

    if category:
        category_exists = db.query(Category).filter(Category.name == category).first()
        if not category_exists:
            return JSONResponse(content={"error": "category doesn't exist"})
        query_1 = query_1.filter(Category.name == category)
        query_2 = query_2.filter(Category.name == category)

    results_1 = query_1.group_by(Category.name).all()
    results_2 = query_2.group_by(Category.name).all()

    comparison_data = {
        "range_1": {category: revenue for category, revenue in results_1},
        "range_2": {category: revenue for category, revenue in results_2}
    }

    return comparison_data
