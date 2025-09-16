import pandas as pd
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
        pma_pmn_idx = header.index('pma_pmn_number')

        for row in reader:
            event_type = row[event_type_idx].strip().upper()
            if event_type != 'DEATH':
                continue

            # Check if it's a 510(k) device
            pma_pmn = row[pma_pmn_idx]
            if not pma_pmn or not str(pma_pmn).strip().upper().startswith('K'):
                continue

            # Extract device info
            device_str = row[device_idx]
            brand_name = None
            if device_str:
                try:
                    device_list = ast.literal_eval(device_str)
                    if isinstance(device_list, list) and len(device_list) > 0:
                        brand_name = device_list[0].get('brand_name')
                except Exception:
                    continue

            # Extract event narrative
            try:
                mdr_text_list = ast.literal_eval(row[mdr_text_idx])
                event_narrative = None
                manufacturer_narrative = None
                
                for entry in mdr_text_list:
                    if entry.get('text_type_code') == 'Description of Event or Problem':
                        event_narrative = entry.get('text')
                    elif entry.get('text_type_code') == 'Additional Manufacturer Narrative':
                        manufacturer_narrative = entry.get('text')

                results.append({
                    'Brand Name': brand_name,
                    'K Number': pma_pmn,
                    'Event Narrative': event_narrative,
                    'Manufacturer Narrative': manufacturer_narrative
                })
                
                print(f"Found 510(k) death case: {brand_name} - {pma_pmn}")
                
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue

    # Save results
    if results:
        results_df = pd.DataFrame(results)
        output_file = 'death_cases_510k_devices.xlsx'
        results_df.to_excel(output_file, index=False)
        print(f'\nAnalysis complete. Found {len(results)} death cases for 510(k) devices.')
        print(f'Results saved to: {output_file}')
        
        # Print summary of device types
        print("\nDevice types involved in death cases:")
        for idx, row in results_df.groupby('Brand Name').size().items():
            print(f"{idx}: {row} cases")
    else:
        print('\nNo 510(k) death cases found.')

if __name__ == "__main__":
    main()
