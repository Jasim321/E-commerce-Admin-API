from fastapi import FastAPI
from app.routes import sales, products, inventories

app = FastAPI()
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventories.router)
