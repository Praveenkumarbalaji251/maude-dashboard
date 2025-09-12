import csv
import ast

csv_path = 'maude_AUG2024_JULY2025.csv'

# Check if 'brand_name' is present in the device field for the first 10 rows
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        device_idx = header.index('device')
    except ValueError:
        print('No device column found!')
        device_idx = None

    if device_idx is not None:
        print('Checking for brand_name in device field (first 10 rows):')
        count = 0
        for row in reader:
            if count >= 10:
                break
            device_str = row[device_idx]
            has_brand_name = False
            brand_name_val = None
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        has_brand_name = 'brand_name' in device_list[0]
                        brand_name_val = device_list[0].get('brand_name')
                except Exception as e:
                    has_brand_name = f'Error: {e}'
            print(f"Row {count+1}: brand_name present? {has_brand_name} | Value: {brand_name_val}")
            count += 1
