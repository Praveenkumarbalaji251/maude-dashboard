import csv
import ast

csv_path = 'maude_AUG2024_JULY2025.csv'
count = 0
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    device_idx = header.index('device')
    event_type_idx = header.index('event_type')
    mdr_text_idx = header.index('mdr_text')
    for row in reader:
        event_type = row[event_type_idx].strip().upper()
        if event_type != 'DEATH':
            continue
        device_str = row[device_idx]
        brand_name = None
        if device_str:
            try:
import csv
import json

csv_path = 'maude_AUG2024_JULY2025.csv'
count = 0
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    device_idx = header.index('device')
    event_type_idx = header.index('event_type')
    mdr_text_idx = header.index('mdr_text')
    for row in reader:
        event_type = row[event_type_idx].strip().upper()
        if event_type != 'DEATH':
            continue
        device_str = row[device_idx]
        brand_name = None
        if device_str:
            try:
                # Safer alternative: parse as JSON if possible
                device_list = json.loads(device_str)
                if isinstance(device_list, list) and len(device_list) > 0:
                    brand_name = device_list[0].get('brand_name')
            except (json.JSONDecodeError, KeyError, TypeError, IndexError):
                brand_name = None
        if brand_name and 'CADD-SOLIS AMBULATORY INFUSION PUMP' in brand_name:
            print(f"Brand: {brand_name}\nMDR Text: {row[mdr_text_idx]}\n{'-'*60}")
            count += 1
            if count == 2:
                break
