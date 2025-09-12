import pandas as pd
import ast
import calendar
from collections import defaultdict

# Load only the first 100 rows for testing
file_path = 'maude_AUG2024_JULY2025.csv'
data = pd.read_csv(file_path, nrows=100)

def extract_event_month(row):
    for col in ['date_received', 'date_of_event']:
        val = row.get(col)
        if pd.notnull(val):
            strval = str(val)
            if len(strval) >= 6:
                month = strval[4:6]
                if month.isdigit():
                    return calendar.month_name[int(month)]
    return 'Unknown'

harm_map = defaultdict(int)
results = []
if 'patient' in data.columns:
    for idx, row in data.iterrows():
        patient_str = row.get('patient')
        brand_name = None
        manufacturer_g_name = None
        event_month = extract_event_month(row)
        if patient_str:
            try:
                patient_data = ast.literal_eval(patient_str)
                if isinstance(patient_data, list):
                    for entry in patient_data:
                        if isinstance(entry, dict):
                            harms = entry.get('patient_problems', [])
                            brand_name = entry.get('brand_name', None)
                            manufacturer_g_name = entry.get('manufacturer_d_name', None)
                            for harm in harms:
                                key = (harm, brand_name, manufacturer_g_name, event_month)
                                harm_map[key] += 1
            except Exception:
                continue
    for (harm, brand, manufacturer, month), count in harm_map.items():
        results.append({
            'Patient Harm': harm,
            'Brand Name': brand,
            'Manufacturer Name': manufacturer,
            'Month': month,
            'Count': count
        })
    df_harm = pd.DataFrame(results)
    df_harm.to_excel('patient_harm_brand_manufacturer_month_test.xlsx', index=False)
    print("\nSaved mapping to patient_harm_brand_manufacturer_month_test.xlsx")
else:
    print("'patient' column not found in the data.")
