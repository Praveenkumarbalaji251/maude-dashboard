import csv
import ast
import pandas as pd

# Load patient problems from Excel file
excel_path = 'patient_problem_counts.xlsx'
try:
    df_patient = pd.read_excel(excel_path)
    if 'Patient Problem' not in df_patient.columns:
        print(f"Error: 'Patient Problem' column not found in {excel_path}")
        exit(1)
    patient_problems_set = set(df_patient['Patient Problem'].dropna())
except FileNotFoundError:
    print(f"Error: Excel file '{excel_path}' not found")
    exit(1)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

csv_path = 'maude_AUG2024_JULY2025.csv'

# Prepare to collect brand_name and patient problems for first 100 rows
results = []


try:
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        try:
            device_idx = header.index('device')
            patient_idx = header.index('patient')
        except ValueError as e:
            print(f'Column not found: {e}')
            exit(1)

        if device_idx is not None and patient_idx is not None:
            count = 0
            for row in reader:
                if count >= 100:
                    break
                # Extract brand_name
                device_str = row[device_idx]
                brand_name = None
                if device_str:
                    try:
                        device_list = ast.literal_eval(device_str)
                        if isinstance(device_list, list) and len(device_list) > 0:
                            brand_name = device_list[0].get('brand_name')
                    except (ValueError, SyntaxError, TypeError) as e:
                        import sys
                        print(f"Error parsing device_str at row {count}: {device_str!r} | {e}", file=sys.stderr)
                        brand_name = None
                # Extract patient problems
                patient_str = row[patient_idx]
                problems = []
                if patient_str:
                    try:
                        patient_list = ast.literal_eval(patient_str)
                        if isinstance(patient_list, list) and len(patient_list) > 0:
                            for patient_dict in patient_list:
                                probs = patient_dict.get('patient_problems', [])
                                # Only include problems present in the Excel file
                                filtered = [p for p in probs if p in patient_problems_set]
                                problems.extend(filtered)
                    except (ValueError, SyntaxError, TypeError) as e:
                        import sys
                        print(f"Error parsing patient_str at row {count}: {patient_str!r} | {e}", file=sys.stderr)
                        pass
                results.append({'brand_name': brand_name, 'patient_problems': problems})
                count += 1
except FileNotFoundError:
    print(f"Error: CSV file '{csv_path}' not found")
    exit(1)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

# Print results for first 100 rows
for idx, item in enumerate(results):
    print(f"Row {idx+1}: Brand Name: {item['brand_name']} | Patient Problems: {item['patient_problems']}")
