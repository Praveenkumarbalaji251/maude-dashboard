import csv
import ast
import pandas as pd

# Load patient problems from Excel file
excel_path = 'patient_problem_counts.xlsx'
df_patient = pd.read_excel(excel_path)
patient_problems_set = set(df_patient['Patient Problem'].dropna().astype(str))

csv_path = 'maude_AUG2024_JULY2025.csv'

# Prepare to collect brand_name, manufacturer_g1_name, patient problems, and month-year for first 1000 rows
results = []

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
        count = 0
        for row in reader:
            if count >= 1000:
                break
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
            # Extract month-year from date_received (format YYYYMMDD)
            date_received = row[date_received_idx]
            month_year = None
            if date_received and len(str(date_received)) >= 6:
                year = str(date_received)[:4]
                month_num = str(date_received)[4:6]
                try:
                    import calendar
                    month_name = calendar.month_name[int(month_num)]
                    month_year = f"{month_name[:3]} {year}"  # e.g., Aug 2024
                except Exception:
                    month_year = f"{month_num} {year}"
            results.append({
                'brand_name': brand_name,
                'manufacturer_g1_name': manufacturer_g1_name,
                'patient_problems': problems,
                'month_year': month_year
            })
            count += 1

# Save results to Excel
output_df = pd.DataFrame(results)
output_df.to_excel('brand_patient_manufacturer_month_1000.xlsx', index=False)
print("Saved mapping to brand_patient_manufacturer_month_1000.xlsx")
