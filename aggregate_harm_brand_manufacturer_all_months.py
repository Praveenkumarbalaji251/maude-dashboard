"""
Moved to scripts/aggregate_harm_brand_manufacturer_all_months.py
"""
import csv
import sys
import ast
import pandas as pd
from collections import defaultdict
import calendar

# Load patient problems from Excel file
excel_path = 'patient_problem_counts.xlsx'
df_patient = pd.read_excel(excel_path)
patient_problems_set = set(df_patient['Patient Problem'].dropna().astype(str))

csv_path = 'maude_AUG2024_JULY2025.csv'
sys.setrecursionlimit(10000)
csv.field_size_limit(10000000)

# Prepare aggregation for each month
monthly_agg = defaultdict(lambda: defaultdict(int))

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        device_idx = header.index('device')
        patient_idx = header.index('patient')
        manufacturer_g1_name_idx = header.index('manufacturer_g1_name')
        date_received_idx = header.index('date_received')
    except ValueError as e:
        print(f'Column not found: {e}')
        device_idx = None
        patient_idx = None
        manufacturer_g1_name_idx = None
        date_received_idx = None

    if None not in (device_idx, patient_idx, manufacturer_g1_name_idx, date_received_idx):
        for row in reader:
            # Extract month-year from date_received (format YYYYMMDD)
            date_received = row[date_received_idx]
            month_year = None
            if date_received and len(str(date_received)) >= 6:
                year = str(date_received)[:4]
                month_num = str(date_received)[4:6]
                try:
                    month_name = calendar.month_name[int(month_num)]
                    month_year = f"{month_name[:3]} {year}"  # e.g., Aug 2024
                except Exception:
                    month_year = f"{month_num} {year}"
            else:
                continue
            # Extract brand_name
            device_str = row[device_idx]
            brand_name = None
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception:
                    brand_name = None
            # Extract manufacturer_g1_name
            manufacturer_g1_name = row[manufacturer_g1_name_idx] if row[manufacturer_g1_name_idx] else None
            # Extract patient problems
            patient_str = row[patient_idx]
            problems = []
            if patient_str:
                try:
                    patient_list = ast.literal_eval(patient_str)
                    if isinstance(patient_list, list) and len(patient_list) > 0:
                        for patient_dict in patient_list:
                            probs = patient_dict.get('patient_problems', [])
                            filtered = [p for p in probs if p in patient_problems_set]
                            problems.extend(filtered)
                except Exception:
                    pass
            # Aggregate by (harm, brand, manufacturer) for each month
            for harm in problems:
                key = (harm, brand_name, manufacturer_g1_name)
                monthly_agg[month_year][key] += 1

# Save each month's aggregation to a separate Excel file
total_months = sorted(monthly_agg.keys(), key=lambda x: (int(x.split()[1]), list(calendar.month_abbr).index(x.split()[0])))
for month in total_months:
    agg_list = [
        {'Month': month, 'Patient Harm': k[0], 'Brand Name': k[1], 'Manufacturer Name': k[2], 'Count': v}
        for k, v in monthly_agg[month].items()
    ]
    agg_df = pd.DataFrame(agg_list)
    agg_df = agg_df.sort_values(by='Count', ascending=False)
    out_name = f'harm_brand_manufacturer_{month.replace(" ", "_").lower()}.xlsx'
    agg_df.to_excel(out_name, index=False)
    print(f"Saved: {out_name}")
