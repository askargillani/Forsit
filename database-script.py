import sqlite3
from datetime import datetime, timedelta
import random

# Connect to (or create) the database file
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Drop existing tables
cursor.executescript("""
DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS InventoryHistory;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
""")

# Create tables
cursor.executescript("""
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

CREATE TABLE Inventory (
    product_id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE InventoryHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    changed_at DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    sale_date DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
""")

# Insert categories
types = ["Electronics", "Clothing", "Home", "Toys"]
cursor.executemany("INSERT INTO Categories (name) VALUES (?)", [(t,) for t in types])

# Insert products
products = [
    ("iPhone 14", 1, 999.99),
    ("Smart TV 55in", 1, 699.99),
    ("T-shirt (Pack of 3)", 2, 29.99),
    ("Sofa Set", 3, 1200.00),
    ("Lego Star Wars Set", 4, 89.99),
    ("Bluetooth Speaker", 1, 59.99),
    ("Winter Jacket", 2, 149.99)
]
cursor.executemany("INSERT INTO Products (name, category_id, price) VALUES (?, ?, ?)", products)

# Prepare inventory and history
cursor.execute("SELECT id FROM Products")
product_ids = [row[0] for row in cursor.fetchall()]

initial_inventory = {pid: random.randint(50, 150) for pid in product_ids}
simulation_days = 30

for pid, start_qty in initial_inventory.items():
    # Insert initial inventory
    cursor.execute("INSERT INTO Inventory (product_id, quantity) VALUES (?, ?)", (pid, start_qty))

    # Simulate 5-8 inventory changes over past 'simulation_days'
    changes = []
    for _ in range(random.randint(5, 8)):
        days_ago = random.randint(1, simulation_days)
        change_date = datetime.now() - timedelta(days=days_ago)
        quantity_change = random.randint(-10, 20)
        changes.append((change_date, quantity_change))
    # Sort changes by date ascending
    changes.sort(key=lambda x: x[0])
    current_qty = start_qty
    for change_date, qty_change in changes:
        new_qty = max(0, current_qty + qty_change)
        cursor.execute(
            "INSERT INTO InventoryHistory (product_id, quantity_change, new_quantity, changed_at) VALUES (?, ?, ?, ?)",
            (pid, qty_change, new_qty, change_date.strftime("%Y-%m-%d %H:%M:%S"))
        )
        current_qty = new_qty
    # Update Inventory current quantity
    cursor.execute(
        "UPDATE Inventory SET quantity = ?, updated_at = ? WHERE product_id = ?",
        (current_qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pid)
    )

# Insert sales within a 3-month window (Mar-May 2025)
start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 5, 31)
days_span = (end_date - start_date).days

sales_records = []
for pid in product_ids:
    # Generate 10-15 sales per product
    sale_dates = []
    for _ in range(random.randint(10, 15)):
        offset = random.randint(0, days_span)
        sale_dates.append(start_date + timedelta(days=offset))
    # Sort sale dates ascending
    sale_dates.sort()
    for sale_date in sale_dates:
        qty = random.randint(1, 5)
        sales_records.append((pid, qty, sale_date.strftime("%Y-%m-%d %H:%M:%S")))

cursor.executemany(
    "INSERT INTO Sales (product_id, quantity, sale_date) VALUES (?, ?, ?)",
    sales_records
)

conn.commit()
conn.close()

print("ecommerce_admin.db created: inventory history and sales in ascending date order.")
