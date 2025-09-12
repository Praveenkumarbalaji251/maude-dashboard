import csv
import ast
import pandas as pd

# Load patient problems from Excel file
excel_path = 'patient_problem_counts.xlsx'
df_patient = pd.read_excel(excel_path)
patient_problems_set = set(df_patient['Patient Problem'].dropna().astype(str))

csv_path = 'maude_AUG2024_JULY2025.csv'

# Check for any matching patient problems in the first 1000 rows
matches = []
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        patient_idx = header.index('patient')
    except ValueError as e:
        print(f'Column not found: {e}')
        patient_idx = None

    if patient_idx is not None:
        count = 0
        for row in reader:
            if count >= 1000:
                break
            patient_str = row[patient_idx]
            found = []
            if patient_str:
                try:
                    patient_list = ast.literal_eval(patient_str)
                    if isinstance(patient_list, list) and len(patient_list) > 0:
                        for patient_dict in patient_list:
                            probs = patient_dict.get('patient_problems', [])
                            filtered = [p for p in probs if p in patient_problems_set]
                            found.extend(filtered)
                except Exception:
                    pass
            if found:
                matches.append({'row': count+1, 'matching_patient_problems': found})
            count += 1

# Print up to 10 rows with matching patient problems
for item in matches[:10]:
    print(f"Row {item['row']}: Matching Patient Problems: {item['matching_patient_problems']}")
if not matches:
    print("No matching patient problems found in the first 1000 rows.")
