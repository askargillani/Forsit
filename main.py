from fastapi import FastAPI
import api.routes.sales as sales
import api.routes.inventory as inventory

app = FastAPI()
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])