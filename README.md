# E-Commerce Sales & Customer Analytics

An end-to-end exploratory data analysis project that turns multi-table e-commerce data into practical business insights using Python, Pandas, and Matplotlib.

## Business questions

- How do revenue and estimated profit change over time?
- Which product categories and regions contribute most to revenue?
- What is the average order value and estimated profit margin?
- How can customers be grouped using recency, frequency, and spending?
- How should cancelled and returned orders be treated in sales reporting?

## Key capabilities

- Generates a reproducible, relational synthetic dataset across customers, products, orders, and order items.
- Joins multiple tables into an order-line fact table with validation checks.
- Calculates revenue, estimated profit, average order value, and profit margin.
- Analyzes monthly, category, and regional performance.
- Creates exploratory RFM customer segments.
- Exports clean analysis tables and publication-ready PNG charts.
- Includes unit tests for core business logic.

## Technology stack

Python · Pandas · NumPy · Matplotlib · Pytest

## Project structure

```text
01-ecommerce-sales-analytics/
├── data/                       # Generated CSV tables
├── docs/
│   └── data_dictionary.md
├── outputs/                    # Generated analysis results and charts
├── src/
│   ├── analysis.py
│   └── generate_data.py
├── tests/
│   └── test_analysis.py
├── run_analysis.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ecommerce-sales-analytics.git
cd ecommerce-sales-analytics
```

### 2. Create and activate a virtual environment

**Windows**
```bash
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generate data and run the analysis

```bash
python run_analysis.py
```

The script creates the CSV files in `data/` and writes tables, KPI summaries, and charts to `outputs/`.

### 5. Run tests

```bash
pytest -q
```

## Outputs

After running the project, the `outputs/` folder contains:

- `kpi_summary.json`
- `monthly_performance.csv`
- `category_performance.csv`
- `regional_performance.csv`
- `customer_segments.csv`
- `delivered_order_facts.csv`
- `monthly_revenue.png`
- `category_revenue.png`
- `regional_revenue.png`

## Analytical approach and assumptions

- Only orders marked `Delivered` are included in revenue and profit calculations.
- Returned and cancelled orders are excluded from the delivered-sales fact table.
- Shipping cost is allocated to order lines in proportion to each line's net sales.
- Profit is an estimate based on the generated unit-cost field; it excludes overhead, taxes, marketing, and other operating expenses.
- RFM segments use relative thresholds within the generated sample and are intended for exploration, not production targeting.

## Dataset note

The included data is generated synthetically for portfolio demonstration and reproducibility. It is not real customer or business data. Findings from this sample should not be presented as evidence about an actual retailer.

## License

MIT.
