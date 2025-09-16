
import pandas as pd
import json
import calendar
from collections import defaultdict

# Load only the first 100 rows for testing
file_path = 'maude_AUG2024_JULY2025.csv'
data = pd.read_csv(file_path, nrows=100)
def extract_event_month(row):
    import re
    for col in ['date_received', 'date_of_event']:
        val = row.get(col)
        if pd.notnull(val):
            strval = str(val)
            # Try different date patterns
            patterns = [
                r'(\d{4})(\d{2})\d{2}',  # YYYYMMDD
                r'(\d{4})-(\d{2})-\d{2}',  # YYYY-MM-DD
                r'(\d{2})/(\d{2})/\d{4}'   # MM/DD/YYYY
            ]
            for pattern in patterns:
                match = re.match(pattern, strval)
                if match:
                    if pattern.endswith(r'/\d{4}'):  # MM/DD/YYYY
                        month = int(match.group(1))
                    else:  # YYYY patterns
                        month = int(match.group(2))
                    if 1 <= month <= 12:
                        return calendar.month_name[month]
    return 'Unknown'
    return 'Unknown'

harm_map = defaultdict(int)
results = []
if 'patient' in data.columns:
    for idx, row in data.iterrows():
        patient_str = row.get('patient')
        brand_name = None
        brand_name = None
        manufacturer_name = None
        event_month = extract_event_month(row)
        if patient_str:

            try:
                patient_data = json.loads(patient_str)
                # Validate patient_data is a list of dicts with expected keys/types
                if isinstance(patient_data, list):
                    for entry in patient_data:
                        if not isinstance(entry, dict):
                            continue
                        # Only accept expected keys and value types
                        allowed_keys = {'patient_problems', 'brand_name', 'manufacturer_name'}
                        if not set(entry.keys()).issubset(allowed_keys):
                            print(f"Row {idx}: Unexpected keys in patient entry, skipping. Keys: {entry.keys()}")
                            continue
                        harms = entry.get('patient_problems', [])
                        brand_name = entry.get('brand_name', None)
                        manufacturer_name = entry.get('manufacturer_name', None)
                        if not isinstance(harms, list):
                            continue
                        for harm in harms:
                            if not isinstance(harm, str):
                                continue
                            key = (harm, brand_name, manufacturer_name, event_month)
                            harm_map[key] += 1
            except Exception as e:
                print(f"Row {idx}: Error processing patient field, skipping. Error: {e} | Value: {patient_str!r}")
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
