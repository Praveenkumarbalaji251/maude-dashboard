import pandas as pd
import ast

# Load raw MAUDE CSV for device and PMA/PMN number
raw = pd.read_csv('maude_AUG2024_JULY2025.csv', usecols=['device','pma_pmn_number'], low_memory=False)
# Load death cases summary
death = pd.read_excel('death_product_problem_by_device_desc.xlsx').head(100)

# Build lookup dictionary once
def build_pma_lookup():
    lookup = {}
    for _, row in raw.iterrows():
        try:
            device_list = ast.literal_eval(row['device'])
            if isinstance(device_list, list) and len(device_list) > 0:
                brand = device_list[0].get('brand_name')
                if brand and brand not in lookup:
                    lookup[brand] = row['pma_pmn_number']
        except (ValueError, SyntaxError, TypeError):
            continue
    return lookup

pma_lookup = build_pma_lookup()

def get_pma(brand):
    return pma_lookup.get(brand)

death['PMA/PMN Number'] = death['Brand Name'].apply(get_pma)
death_510k = death[death['PMA/PMN Number'].astype(str).str.startswith('K')]
death_510k.to_excel('death_product_problem_by_device_510k.xlsx', index=False)
print('Saved: death_product_problem_by_device_510k.xlsx')
