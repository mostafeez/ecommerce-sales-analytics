"""Reusable analysis functions for the e-commerce analytics project."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_data(data_dir="data"):
    path = Path(data_dir)
    customers = pd.read_csv(path / "customers.csv", parse_dates=["signup_date"])
    products = pd.read_csv(path / "products.csv")
    orders = pd.read_csv(path / "orders.csv", parse_dates=["order_date"])
    items = pd.read_csv(path / "order_items.csv")
    return customers, products, orders, items

def build_order_facts(customers, products, orders, items):
    """Create an order-line fact table; revenue is recognized for delivered orders only."""
    lines = (items.merge(orders, on="order_id", validate="many_to_one")
                  .merge(products, on="product_id", validate="many_to_one")
                  .merge(customers[["customer_id", "region", "customer_segment"]],
                         on="customer_id", validate="many_to_one"))
    lines["gross_sales"] = lines["quantity"] * lines["unit_price"]
    lines["net_sales"] = lines["gross_sales"] * (1 - lines["discount_rate"])
    lines["cost_of_goods"] = lines["quantity"] * lines["unit_cost"]
    lines["line_profit_before_shipping"] = lines["net_sales"] - lines["cost_of_goods"]
    delivered = lines[lines["order_status"].eq("Delivered")].copy()
    # Allocate each order's shipping cost across its lines by line net sales.
    order_sales = delivered.groupby("order_id")["net_sales"].transform("sum").replace(0, 1)
    delivered["allocated_shipping_cost"] = (
        delivered["shipping_cost"] * delivered["net_sales"] / order_sales
    )
    delivered["estimated_profit"] = (
        delivered["net_sales"] - delivered["cost_of_goods"] -
        delivered["allocated_shipping_cost"]
    )
    return delivered

def calculate_kpis(facts, orders):
    revenue = float(facts["net_sales"].sum())
    profit = float(facts["estimated_profit"].sum())
    delivered_orders = int(orders.loc[orders["order_status"].eq("Delivered"), "order_id"].nunique())
    customers = int(facts["customer_id"].nunique())
    return {
        "net_revenue": round(revenue, 2),
        "estimated_profit": round(profit, 2),
        "delivered_orders": delivered_orders,
        "unique_customers": customers,
        "average_order_value": round(revenue / delivered_orders, 2) if delivered_orders else 0,
        "profit_margin_pct": round((profit / revenue) * 100, 2) if revenue else 0
    }

def customer_rfm(facts, snapshot_date=None):
    if facts.empty:
        return pd.DataFrame(columns=["customer_id", "recency_days", "frequency", "monetary", "segment"])
    snapshot = pd.Timestamp(snapshot_date) if snapshot_date else facts["order_date"].max() + pd.Timedelta(days=1)
    rfm = facts.groupby("customer_id").agg(
        last_order=("order_date", "max"),
        frequency=("order_id", "nunique"),
        monetary=("net_sales", "sum")
    ).reset_index()
    rfm["recency_days"] = (snapshot - rfm["last_order"]).dt.days
    # Transparent rule-based groups; thresholds are relative to this sample.
    rfm["segment"] = "Regular"
    rfm.loc[(rfm["frequency"] >= rfm["frequency"].quantile(.75)) &
            (rfm["recency_days"] <= rfm["recency_days"].quantile(.25)), "segment"] = "Loyal"
    rfm.loc[rfm["recency_days"] >= rfm["recency_days"].quantile(.75), "segment"] = "At Risk"
    rfm.loc[(rfm["frequency"] == 1) &
            (rfm["recency_days"] <= rfm["recency_days"].quantile(.25)), "segment"] = "New"
    return rfm[["customer_id", "recency_days", "frequency", "monetary", "segment"]]

def run_analysis(data_dir="data", output_dir="outputs"):
    customers, products, orders, items = load_data(data_dir)
    facts = build_order_facts(customers, products, orders, items)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    kpis = calculate_kpis(facts, orders)
    (out / "kpi_summary.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")

    monthly = (facts.assign(month=facts["order_date"].dt.to_period("M").astype(str))
                    .groupby("month", as_index=False)
                    .agg(net_revenue=("net_sales", "sum"), estimated_profit=("estimated_profit", "sum")))
    category = (facts.groupby("category", as_index=False)
                     .agg(net_revenue=("net_sales", "sum"), estimated_profit=("estimated_profit", "sum"),
                          units_sold=("quantity", "sum"))
                     .sort_values("net_revenue", ascending=False))
    region = (facts.groupby("region", as_index=False)
                   .agg(net_revenue=("net_sales", "sum"), estimated_profit=("estimated_profit", "sum"))
                   .sort_values("net_revenue", ascending=False))
    rfm = customer_rfm(facts)

    monthly.to_csv(out / "monthly_performance.csv", index=False)
    category.to_csv(out / "category_performance.csv", index=False)
    region.to_csv(out / "regional_performance.csv", index=False)
    rfm.to_csv(out / "customer_segments.csv", index=False)
    facts.to_csv(out / "delivered_order_facts.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["month"], monthly["net_revenue"], marker="o")
    plt.title("Monthly Net Revenue")
    plt.xlabel("Month"); plt.ylabel("Net revenue")
    plt.xticks(rotation=60, ha="right"); plt.tight_layout()
    plt.savefig(out / "monthly_revenue.png", dpi=160); plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(category["category"], category["net_revenue"])
    plt.title("Net Revenue by Product Category")
    plt.xlabel("Category"); plt.ylabel("Net revenue")
    plt.xticks(rotation=25, ha="right"); plt.tight_layout()
    plt.savefig(out / "category_revenue.png", dpi=160); plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(region["region"], region["net_revenue"])
    plt.title("Net Revenue by Region")
    plt.xlabel("Region"); plt.ylabel("Net revenue")
    plt.tight_layout(); plt.savefig(out / "regional_revenue.png", dpi=160); plt.close()

    return kpis, monthly, category, region, rfm

if __name__ == "__main__":
    metrics, *_ = run_analysis()
    print("Analysis complete. KPI summary:")
    for key, value in metrics.items():
        print(f"- {key}: {value}")
