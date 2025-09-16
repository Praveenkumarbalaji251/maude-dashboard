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

def extract_problems_from_list(problem_list):
    if not problem_list:
        return []
    try:
        problems = ast.literal_eval(problem_list)
        if isinstance(problems, list):
            patient_problems = []
            for item in problems:
                if isinstance(item, dict):
                    if 'patient_problems' in item:
                        patient_problems.extend(item['patient_problems'])
            return list(set(patient_problems))  # Remove duplicates
    except:
        pass
    return []

def extract_product_problems(problem_list):
    if not problem_list:
        return []
    try:
        problems = ast.literal_eval(problem_list)
        if isinstance(problems, list):
            return list(set(problems))  # Remove duplicates
    except:
        pass
    return []

def main():
    csv_path = 'maude_AUG2024_JULY2025.csv'
    results = []

    required_columns = ['device', 'event_type', 'mdr_text', 'pma_pmn_number', 'patient', 'product_problems']
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except Exception as e:
                print(f"Error reading header from CSV: {e}")
                return

            header_map = {col: idx for idx, col in enumerate(header)}
            missing_columns = [col for col in required_columns if col not in header_map]
            if missing_columns:
                print(f"Error: Missing required columns in CSV: {', '.join(missing_columns)}")
                return

            device_idx = header_map['device']
            event_type_idx = header_map['event_type']
            mdr_text_idx = header_map['mdr_text']
            pma_pmn_idx = header_map['pma_pmn_number']
            patient_idx = header_map['patient']
            product_problems_idx = header_map['product_problems']

            for row in reader:
                # Ensure row has enough columns to avoid IndexError
                min_required = max(device_idx, event_type_idx, mdr_text_idx,
                                  pma_pmn_idx, patient_idx, product_problems_idx)
                if len(row) <= min_required:
                    print(f"Skipping malformed row (too few columns): {row}")
                    continue
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

                # Extract patient problems
                patient_problems = extract_problems_from_list(row[patient_idx])
                
                # Extract product problems
                product_problems = extract_product_problems(row[product_problems_idx])

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
                        'Patient Problems': '; '.join(patient_problems) if patient_problems else '',
                        'Product Problems': '; '.join(product_problems) if product_problems else '',
                        'Event Narrative': event_narrative,
                        'Manufacturer Narrative': manufacturer_narrative
                    })
                    
                    print(f"Found 510(k) death case: {brand_name} - {pma_pmn}")
                    print(f"Patient Problems: {', '.join(patient_problems) if patient_problems else 'None'}")
                    print(f"Product Problems: {', '.join(product_problems) if product_problems else 'None'}")
                    print("-" * 80)
                    
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_path}' not found.")
        return
    except IOError as e:
        print(f"Error opening CSV file: {e}")
        return

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

            # Extract patient problems
            patient_problems = extract_problems_from_list(row[patient_idx])
            
            # Extract product problems
            product_problems = extract_product_problems(row[product_problems_idx])

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
                    'Patient Problems': '; '.join(patient_problems) if patient_problems else '',
                    'Product Problems': '; '.join(product_problems) if product_problems else '',
                    'Event Narrative': event_narrative,
                    'Manufacturer Narrative': manufacturer_narrative
                })
                
                print(f"Found 510(k) death case: {brand_name} - {pma_pmn}")
                print(f"Patient Problems: {', '.join(patient_problems) if patient_problems else 'None'}")
                print(f"Product Problems: {', '.join(product_problems) if product_problems else 'None'}")
                print("-" * 80)
                
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue

    # Save results
    if results:
        results_df = pd.DataFrame(results)
        output_file = 'death_cases_510k_devices_with_problems.xlsx'
        results_df.to_excel(output_file, index=False)
        print(f'\nAnalysis complete. Found {len(results)} death cases for 510(k) devices.')
        print(f'Results saved to: {output_file}')
        
        # Print summary of device types
        print("\nDevice types involved in death cases:")
        for idx, row in results_df.groupby('Brand Name').size().items():
            print(f"{idx}: {row} cases")
            
        # Print summary of common patient problems
        all_patient_problems = []
        for problems in results_df['Patient Problems'].dropna():
            all_patient_problems.extend(problems.split('; '))
        
        if all_patient_problems:
            print("\nMost common patient problems:")
            problem_counts = pd.Series(all_patient_problems).value_counts()
            for problem, count in problem_counts.head(10).items():
                print(f"{problem}: {count} cases")
            
        # Print summary of common product problems
        all_product_problems = []
        for problems in results_df['Product Problems'].dropna():
            all_product_problems.extend(problems.split('; '))
            
        if all_product_problems:
            print("\nMost common product problems:")
            problem_counts = pd.Series(all_product_problems).value_counts()
            for problem, count in problem_counts.head(10).items():
                print(f"{problem}: {count} cases")
    else:
        print('\nNo 510(k) death cases found.')

if __name__ == "__main__":
    main()
