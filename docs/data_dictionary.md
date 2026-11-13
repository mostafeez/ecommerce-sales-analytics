# Data Dictionary

All records in `data/` are **synthetic demonstration data** generated with a fixed random seed. They do not represent a real company, customer, or transaction.

| File | Grain | Key fields |
|---|---|---|
| `customers.csv` | One row per customer | customer_id, signup_date, region, customer_segment |
| `products.csv` | One row per product | product_id, product_name, category, unit_cost, list_price |
| `orders.csv` | One row per order | order_id, customer_id, order_date, order_status, payment_method, discount_rate, shipping_cost |
| `order_items.csv` | One row per order-product line | order_id, product_id, quantity, unit_price |

## Metric definitions

- **Net revenue:** quantity × unit price × (1 − order discount), for delivered orders only.
- **Estimated profit:** net revenue less estimated product cost and allocated shipping cost.
- **Average order value:** delivered-order net revenue divided by delivered order count.
- **Profit margin:** estimated profit divided by net revenue.
- **RFM:** rule-based recency, frequency, and monetary summaries. Segment labels are exploratory, not predictive.
