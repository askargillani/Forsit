from sqlalchemy.orm import Session
from sqlalchemy import func
from models.sale import Sale
from models.products import Product
from models.categories import Category
from models.inventory import Inventory
from models.inventoryHistory import InventoryHistory
class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_revenue_by_period(self, start_date, end_date):
        revenue = (
            self.db.query(func.sum(Sale.quantity * Product.price))
            .join(Product, Sale.product_id == Product.id)
            .filter(Sale.sale_date >= start_date)
            .filter(Sale.sale_date <= end_date)
            .scalar()
        )
        return revenue or 0
    
    def get_top_products(self, start_date, end_date):

        top_products = (
            self.db.query(Product.name, func.sum(Sale.quantity).label("total_quantity"))
            .join(Sale, Sale.product_id == Product.id)
            .filter(Sale.sale_date >= start_date)
            .filter(Sale.sale_date <= end_date)
            .group_by(Product.name)
            .order_by(func.sum(Sale.quantity).desc())
            .limit(5)
            .all()
        )
        return [{"product_name": name, "total_quantity": total_quantity} for name, total_quantity in top_products]

    def get_revenue_by_category(self, start_date=None, end_date=None):
        query = (
            self.db.query(
                Category.name.label("category"),
                func.sum(Sale.quantity * Product.price).label("revenue")
            )
            .join(Product, Product.category_id == Category.id)
            .join(Sale, Sale.product_id == Product.id)
            .order_by(func.sum(Sale.quantity * Product.price).desc())
        )
        if start_date is not None:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date is not None:
            query = query.filter(Sale.sale_date <= end_date)
        query = query.group_by(Category.name)
        results = query.all()
        return [{"category": category, "revenue": float(revenue or 0)} for category, revenue in results]

    def get_inventory_history(self, product_name, start_date=None, end_date=None):
        product = self.db.query(Product).filter(Product.name == product_name).first()
        id = product.id if product else None
        if id:
            query = self.db.query(
                InventoryHistory.changed_at,
                InventoryHistory.quantity_change,
                InventoryHistory.new_quantity
            ).filter(InventoryHistory.product_id == id)
            if start_date is not None:
                query = query.filter(InventoryHistory.changed_at >= start_date)
            if end_date is not None:
                query = query.filter(InventoryHistory.changed_at <= end_date)
            results = query.all()
        else:
            results = []
        

        return [
            {
                "date": date.strftime("%Y-%m-%d"),
                "change": change,
                "new_quantity": new_quantity
            }
            for date, change, new_quantity in results
        ]

    def update_inventory(self, product_name, quantity_change):
        product = self.db.query(Product).filter(Product.name == product_name).first()
        id = product.id if product else None
        if(id):
            self.db.query(Inventory).filter(Inventory.product_id == id).update({"quantity": Inventory.quantity + quantity_change, "updated_at": func.now()})
            self.db.commit()
            inventory = self.db.query(Inventory).filter(Inventory.product_id == id).first()
            new_quantity = inventory.quantity + quantity_change
            self.db.add(InventoryHistory(product_id=product.id, quantity_change=quantity_change, new_quantity=new_quantity, changed_at=func.now()))
            self.db.commit()
            return new_quantity
        else:
            return new_quantity


    def get_inventory(self, product_name=None):
        product = self.db.query(Product).filter(Product.name == product_name).first()
        if product:
            id = product.id
            results = (
                self.db.query(Product.name.label("name"), Inventory.quantity.label("quantity"), Inventory.updated_at)
                .join(Inventory, Inventory.product_id == Product.id)
                .filter(Product.id == id)
                .all()
            )
        return [
            {
                "product": name,
                "quantity": quantity,
                "updated_at": updated_at.isoformat() if updated_at else None
            }
            for name, quantity, updated_at in results
        ]
    
    def get_low_stock(self, threshold):
        results = (
            self.db.query(Product.name.label("name"), Inventory.quantity.label("quantity"))
            .join(Product, Inventory.product_id == Product.id).
            filter(Inventory.quantity < threshold)
            .all()
        )
        return [
            {"product": name, "quantity": quantity}
            for name, quantity in results
        ]
    
    def add_product(self, product_name, quantity, category, price):
        cateogoryId = self.db.query(Category).filter(Category.name == category).first()
        productName = self.db.query(Product).filter(Product.name == product_name).first()
        if cateogoryId and not productName:
            product = Product(name=product_name, price=price, category_id=cateogoryId.id)
            self.db.add(product)
            self.db.commit()
            inventory = Inventory(product_id=product.id, quantity=quantity)
            self.db.add(inventory)
            self.db.commit()
        else:
            if productName:
                return {"error": "Product already exists"}
            return {"error": "Category not found"}
        return {"product_id": product.id, "product_name": product.name, "quantity": inventory.quantity}
