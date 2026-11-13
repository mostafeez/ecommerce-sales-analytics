import pandas as pd
from src.analysis import build_order_facts, calculate_kpis, customer_rfm

def sample_tables():
    customers = pd.DataFrame({
        "customer_id": ["C1", "C2"], "region": ["North", "South"],
        "customer_segment": ["Consumer", "Corporate"]
    })
    products = pd.DataFrame({
        "product_id": ["P1"], "product_name": ["Item"], "category": ["Home"],
        "unit_cost": [5.0], "list_price": [10.0]
    })
    orders = pd.DataFrame({
        "order_id": ["O1", "O2"], "customer_id": ["C1", "C2"],
        "order_date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "order_status": ["Delivered", "Cancelled"], "payment_method": ["Card", "Cash"],
        "discount_rate": [0.1, 0.0], "shipping_cost": [2.0, 2.0]
    })
    items = pd.DataFrame({
        "order_id": ["O1", "O2"], "product_id": ["P1", "P1"],
        "quantity": [2, 1], "unit_price": [10.0, 10.0]
    })
    return customers, products, orders, items

def test_cancelled_orders_are_excluded():
    facts = build_order_facts(*sample_tables())
    assert facts["order_id"].unique().tolist() == ["O1"]

def test_kpi_calculation():
    customers, products, orders, items = sample_tables()
    facts = build_order_facts(customers, products, orders, items)
    kpis = calculate_kpis(facts, orders)
    assert kpis["delivered_orders"] == 1
    assert kpis["unique_customers"] == 1
    assert kpis["net_revenue"] == 18.0

def test_rfm_returns_customer_segments():
    customers, products, orders, items = sample_tables()
    facts = build_order_facts(customers, products, orders, items)
    rfm = customer_rfm(facts)
    assert {"recency_days", "frequency", "monetary", "segment"}.issubset(rfm.columns)
