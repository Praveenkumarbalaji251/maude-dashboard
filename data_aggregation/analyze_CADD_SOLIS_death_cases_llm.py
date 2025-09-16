import pandas as pd
import ast
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
if not client.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Load the filtered death cases for CADD-SOLIS
filtered_df = pd.read_excel('death_cases_CADD_SOLIS.xlsx')

# Load the source CSV to get event text
csv_path = 'maude_AUG2024_JULY2025.csv'
results = []

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    import csv
    reader = csv.reader(f)
    header = next(reader)
    # Find relevant columns
    try:
        device_idx = header.index('device')
        event_text_idx = header.index('event_text') if 'event_text' in header else None
    except ValueError as e:
        print(f'Column not found: {e}')
        device_idx = None
        event_text_idx = None

    if None not in (device_idx, event_text_idx):
        for row in reader:
            device_str = row[device_idx]
            brand_name = None
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception:
                    brand_name = None
            if brand_name and 'CADD-SOLIS AMBULATORY INFUSION PUMP' in brand_name:
                event_text = row[event_text_idx]
                # Send to LLM
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a medical device safety expert."},
                            {"role": "user", "content": f"Read the following event text and determine if the death was likely caused by the device. Provide a short summary and your reasoning.\n\nEvent Text: {event_text}"}
                        ],
                        max_tokens=200
                    )
                    summary = response.choices[0].message.content
                    time.sleep(1)
                except Exception as e:
                    print(f"OpenAI API error: {e}")
                    summary = f"Error processing: {str(e)}"
                results.append({
                    'Brand Name': brand_name,
                    'Event Text': event_text,
                    'LLM Summary': summary
                })

# Save results to Excel
results_df = pd.DataFrame(results)
results_df.to_excel('CADD_SOLIS_death_cases_LLM.xlsx', index=False)
print('Saved: CADD_SOLIS_death_cases_LLM.xlsx')
