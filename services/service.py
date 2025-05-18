from repository.repository import Repository
from schemas.response.revenue_comparison_response import RevenueResponse
from schemas.response.top_products_response import TopProductResponse
from schemas.response.by_category_response import ByCategoryResponse
from schemas.response.inventory_history_response import InventoryHistoryResponse
from schemas.response.inventory_update_response import InventoryUpdateResponse
from schemas.response.inventory_list_response import InventoryListResponse
from schemas.response.low_stock_response import LowStockResponse

class Service:
    def __init__(self, db):
        self.repo = Repository(db)

    def get_revenue_by_period(self, start_date, end_date):
        return self.repo.get_revenue_by_period(start_date, end_date)
    
    def get_revenue_comparison(self, start_date1, end_date1, start_date2, end_date2):
        revenue1 = self.repo.get_revenue_by_period(start_date1, end_date1)
        revenue2 = self.repo.get_revenue_by_period(start_date2, end_date2)
        return RevenueResponse(
            revenue1=revenue1,
            revenue2=revenue2,
            change=revenue2 - revenue1
        )
    
    def get_top_products(self, start_date, end_date):
        products = self.repo.get_top_products(start_date, end_date)
        return [TopProductResponse(**prod) for prod in products]

    def get_revenue_by_category(self, start_date=None, end_date=None):
        data = self.repo.get_revenue_by_category(start_date, end_date)
        return [ByCategoryResponse(**item) for item in data]

    def get_inventory_history(self, product_name, start_date=None, end_date=None):
        data = self.repo.get_inventory_history(product_name, start_date, end_date)
        return [InventoryHistoryResponse(**item) for item in data]

    def update_inventory(self, product_name, quantity_change):
        new_quantity = self.repo.update_inventory(product_name, quantity_change)
        return InventoryUpdateResponse(
            product_name=product_name,
            new_quantity=new_quantity,
            status="updated"
        )

    def get_inventory(self, product_name=None):
        data = self.repo.get_inventory(product_name)
        return [InventoryListResponse(**item) for item in data]

    def get_low_stock(self, threshold):
        data = self.repo.get_low_stock(threshold)
        return [LowStockResponse(**item) for item in data]
    
    def add_product(self, product_name, quantity, category, price):
        result = self.repo.add_product(product_name, quantity, category, price)
        return {"result": result}

