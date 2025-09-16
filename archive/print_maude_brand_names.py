import csv
import ast

csv_path = 'maude_AUG2024_JULY2025.csv'

# Find the column index for 'device' (the nested field)
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        device_idx = header.index('device')
    except ValueError:
        print('No device column found!')
        device_idx = None

    if device_idx is not None:
        print('First 10 brand_name values from device field:')
        count = 0
        for row in reader:
            if count >= 10:
                break
            device_str = row[device_idx]
            brand_name = None
            if device_str:
                try:
                    # device_str is a list of dicts as a string
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception as e:
                    brand_name = f'Error: {e}'
            print(f"Row {count+1}: {brand_name}")
            count += 1
