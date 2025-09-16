import pandas as pd
from openai import OpenAI
import ast
import csv
import sys

# Increase CSV field size limit
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

import os

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
client = OpenAI(api_key=api_key)

def analyze_event(event_narrative):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical device safety expert."},
                {"role": "user", "content": f"Read the following event narrative and determine if the death was likely caused by the device. Focus only on the event narrative, not manufacturer narrative. Provide a short summary and your reasoning.\n\nEvent Narrative: {event_narrative}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in LLM analysis: {str(e)}")
        return None

def main():
    csv_path = 'maude_AUG2024_JULY2025.csv'
    results = []

    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Get column indices
        device_idx = header.index('device')
        event_type_idx = header.index('event_type')
        mdr_text_idx = header.index('mdr_text')

        for row in reader:
            event_type = row[event_type_idx].strip().upper()
            if event_type != 'DEATH':
                continue

            # Extract brand name
            device_str = row[device_idx]
            brand_name = None
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception:
                    continue

            if brand_name and 'CADD-SOLIS AMBULATORY INFUSION PUMP' in brand_name:
                # Extract event narrative
                try:
                    mdr_text_list = ast.literal_eval(row[mdr_text_idx])
                    event_narrative = None
                    for entry in mdr_text_list:
                        if entry.get('text_type_code') == 'Description of Event or Problem':
                            event_narrative = entry.get('text')
                            break

                    if event_narrative:
                        print(f"\nProcessing event for {brand_name}...")
                        summary = analyze_event(event_narrative)
                        if summary:
                            results.append({
                                'Brand Name': brand_name,
                                'Event Narrative': event_narrative,
                                'LLM Summary': summary
                            })
                            print("Analysis complete.")
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue

    # Save results
    if results:
        results_df = pd.DataFrame(results)
        output_file = 'CADD_SOLIS_death_cases_analysis.xlsx'
        results_df.to_excel(output_file, index=False)
        print(f'\nAnalysis complete. Results saved to: {output_file}')
    else:
        print('\nNo results found.')

if __name__ == "__main__":
    main()
