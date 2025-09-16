

import pandas as pd
import openai
import ast
import csv
import json
import sys

import os
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")


csv_path = 'maude_AUG2024_JULY2025.csv'
if not os.path.exists(csv_path):
    print(f"Error: CSV file '{csv_path}' not found")
    sys.exit(1)
results = []

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        device_idx = header.index('device')
        event_type_idx = header.index('event_type')
        mdr_text_idx = header.index('mdr_text')
    except ValueError as e:
        print(f"Error: Required column not found in CSV: {e}")
        sys.exit(1)
    for row in reader:
        event_type = row[event_type_idx].strip().upper()
        if event_type != 'DEATH':
            continue
        device_str = row[device_idx]
        brand_name = None
        if device_str:
            try:
                # Ensure valid JSON: strip, replace single quotes with double quotes if needed
                device_str_clean = device_str.strip().replace("'", '"')
                device_list = json.loads(device_str_clean)
                if isinstance(device_list, list) and len(device_list) > 0:
                    brand_name = device_list[0].get('brand_name')
                else:
                    brand_name = None
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Malformed device field: {device_str!r} | Error: {e}")
                brand_name = None
        if brand_name and 'CADD-SOLIS AMBULATORY INFUSION PUMP' in brand_name:
            try:
                mdr_text_list = ast.literal_eval(row[mdr_text_idx])
                # Add the filtered record to results
                results.append({
                    'device': device_str,
                    'brand_name': brand_name,
                    'event_type': event_type,
                    'mdr_text': mdr_text_list
                })
            except Exception:
                continue  # Skip rows with malformed mdr_text

results_df = pd.DataFrame(results)
results_df.to_excel('CADD_SOLIS_death_cases_LLM_event_narrative.xlsx', index=False)
print('Saved: CADD_SOLIS_death_cases_LLM_event_narrative.xlsx')
