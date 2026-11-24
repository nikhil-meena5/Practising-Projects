"""
generate_sample_data.py
Creates sales_data.xlsx  ->  the sample sheet you give to the intern.
Columns: Date, Product, Quantity, Price, City   (150 rows, Jan-Jun 2026)
Run:  python generate_sample_data.py
"""
import random
from datetime import date, timedelta

import pandas as pd

random.seed(42)  # same data every time, so everyone gets the same totals

PRODUCTS = {            # product -> unit price (Rs)
    "Laptop": 55000,
    "Smartphone": 20000,
    "Tablet": 25000,
    "Smartwatch": 8000,
    "Headphones": 2500,
    "Keyboard": 1500,
}
# weights make cheaper items sell in higher quantities (more realistic)
WEIGHTS = [1, 3, 2, 3, 6, 6]
CITIES = ["Jaipur", "Delhi", "Mumbai", "Bengaluru", "Pune"]

start, end = date(2026, 1, 1), date(2026, 6, 30)
days = (end - start).days

rows = []
for _ in range(150):
    product = random.choices(list(PRODUCTS), weights=WEIGHTS)[0]
    rows.append({
        "Date": start + timedelta(days=random.randint(0, days)),
        "Product": product,
        "Quantity": random.randint(1, 5),
        "Price": PRODUCTS[product],
        "City": random.choice(CITIES),
    })

df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
df.to_excel("sales_data.xlsx", index=False, sheet_name="Sales")
print(f"Created sales_data.xlsx with {len(df)} rows")
