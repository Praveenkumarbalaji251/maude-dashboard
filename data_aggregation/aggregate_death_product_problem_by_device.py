import csv
import ast
import pandas as pd
from collections import defaultdict

csv_path = 'maude_AUG2024_JULY2025.csv'
csv.field_size_limit(10000000)

# Prepare aggregation for death cases by product problem, brand, manufacturer
death_problem_agg = defaultdict(int)

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        device_idx = header.index('device')
        manufacturer_g1_name_idx = header.index('manufacturer_g1_name')
        event_type_idx = header.index('event_type')
        product_problem_idx = header.index('product_problems')
    except ValueError as e:
        print(f'Column not found: {e}')
        print('Required columns missing. Exiting.')
        exit(1)
    if None not in (device_idx, manufacturer_g1_name_idx, event_type_idx, product_problem_idx):
        for row in reader:
            event_type = row[event_type_idx].strip().upper()
            if event_type != 'DEATH':
        for row in reader:
            if len(row) <= max(device_idx, manufacturer_g1_name_idx, event_type_idx, product_problem_idx):
                continue  # Skip malformed rows
            event_type = row[event_type_idx].strip().upper()
            if event_type != 'DEATH':
                continue
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception:
                    brand_name = None
            # Extract manufacturer_g1_name
            manufacturer_g1_name = row[manufacturer_g1_name_idx] if row[manufacturer_g1_name_idx] else None
            # Extract product problems
            product_problem_str = row[product_problem_idx]
            product_problems = []
            if product_problem_str:
                try:
                    product_problems = ast.literal_eval(product_problem_str)
                    if not isinstance(product_problems, list):
                        product_problems = [product_problems]
                except Exception:
                    product_problems = [product_problem_str]
            # Aggregate by (product_problem, brand, manufacturer) for death cases
            for problem in product_problems:
                # Fix: convert dicts to string for hashing
                if isinstance(problem, dict):
                    problem = str(problem)
                key = (problem, brand_name, manufacturer_g1_name)
                death_problem_agg[key] += 1

# Save death case aggregation by product problem to Excel
agg_list = [
    {'Product Problem': k[0], 'Brand Name': k[1], 'Manufacturer Name': k[2], 'Death Count': v}
    for k, v in death_problem_agg.items()
]
agg_df = pd.DataFrame(agg_list)
agg_df = agg_df.sort_values(by='Death Count', ascending=False)
agg_df.to_excel('death_product_problem_by_device.xlsx', index=False)
print('Saved: death_product_problem_by_device.xlsx')
