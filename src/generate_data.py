"""Generate deterministic synthetic e-commerce data for the project."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42

def generate_dataset(output_dir="data", n_customers=350, n_orders=1100):
    rng = np.random.default_rng(SEED)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    regions = ["North", "South", "East", "West", "Central"]
    categories = {
        "Electronics": ["Wireless Earbuds", "Laptop Stand", "Keyboard", "Monitor", "Power Bank"],
        "Home & Living": ["Desk Lamp", "Storage Box", "Water Bottle", "Bedsheet", "Coffee Maker"],
        "Fashion": ["Backpack", "Sneakers", "T-Shirt", "Hoodie", "Wallet"],
        "Beauty": ["Face Wash", "Moisturizer", "Sunscreen", "Hair Dryer", "Perfume"],
        "Sports": ["Yoga Mat", "Dumbbell Set", "Running Belt", "Fitness Band", "Skipping Rope"],
    }
    product_rows = []
    pid = 1
    for category, names in categories.items():
        for name in names:
            cost = float(rng.uniform(5, 120))
            product_rows.append({
                "product_id": f"P{pid:03d}", "product_name": name,
                "category": category, "unit_cost": round(cost, 2),
                "list_price": round(cost * rng.uniform(1.35, 2.25), 2)
            })
            pid += 1
    products = pd.DataFrame(product_rows)

    customer_dates = pd.to_datetime("2023-10-01") + pd.to_timedelta(
        rng.integers(0, 500, n_customers), unit="D"
    )
    customers = pd.DataFrame({
        "customer_id": [f"C{i:04d}" for i in range(1, n_customers + 1)],
        "signup_date": customer_dates,
        "region": rng.choice(regions, n_customers, p=[.22, .18, .20, .22, .18]),
        "customer_segment": rng.choice(["Consumer", "Small Business", "Corporate"],
                                       n_customers, p=[.68, .22, .10])
    })

    # Give a subset of customers a higher chance of repeat purchases.
    customer_weights = rng.gamma(shape=1.5, scale=1.0, size=n_customers)
    customer_weights = customer_weights / customer_weights.sum()
    order_dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 730, n_orders), unit="D"
    )
    selected_customers = rng.choice(customers["customer_id"], n_orders, p=customer_weights)
    order_rows, item_rows = [], []
    for i in range(n_orders):
        order_id = f"O{i+1:05d}"
        status = rng.choice(["Delivered", "Returned", "Cancelled"], p=[.91, .055, .035])
        discount = float(rng.choice([0, .05, .10, .15, .20], p=[.25, .25, .25, .18, .07]))
        shipping_cost = float(rng.uniform(1.5, 9.0))
        order_rows.append({
            "order_id": order_id, "customer_id": selected_customers[i],
            "order_date": order_dates[i], "order_status": status,
            "payment_method": rng.choice(["Card", "Digital Wallet", "Cash on Delivery", "Bank Transfer"]),
            "discount_rate": discount, "shipping_cost": round(shipping_cost, 2)
        })
        n_lines = int(rng.integers(1, 5))
        chosen = rng.choice(products.index, n_lines, replace=False)
        for idx in chosen:
            product = products.iloc[idx]
            quantity = int(rng.integers(1, 4))
            unit_price = float(product["list_price"] * rng.uniform(.92, 1.08))
            item_rows.append({
                "order_id": order_id, "product_id": product["product_id"],
                "quantity": quantity, "unit_price": round(unit_price, 2)
            })

    orders = pd.DataFrame(order_rows)
    items = pd.DataFrame(item_rows)
    customers.to_csv(out / "customers.csv", index=False, date_format="%Y-%m-%d")
    products.to_csv(out / "products.csv", index=False)
    orders.to_csv(out / "orders.csv", index=False, date_format="%Y-%m-%d")
    items.to_csv(out / "order_items.csv", index=False)
    return customers, products, orders, items

if __name__ == "__main__":
    generate_dataset()
    print("Synthetic e-commerce tables generated in ./data")
