import pandas as pd
import glob

# Find all monthly Excel files
files = glob.glob('harm_brand_manufacturer_*.xlsx')

if not files:
    raise FileNotFoundError("No files matching pattern 'harm_brand_manufacturer_*.xlsx' found")
dfs = []
for f in files:
    try:
        temp_df = pd.read_excel(f)
        if temp_df.empty:
            print(f"Warning: {f} is empty, skipping")
            continue
        # Validate expected columns exist
        required_columns = ['Patient Harm', 'Brand Name', 'Manufacturer Name', 'Count']
        missing_cols = [col for col in required_columns if col not in temp_df.columns]
        if missing_cols:
            raise ValueError(f"File {f} missing required columns: {missing_cols}")
        dfs.append(temp_df)
    except Exception as e:
        print(f"Error processing {f}: {e}")
        raise

if not dfs:
    raise ValueError("No valid data files found to process")

df = pd.concat(dfs, ignore_index=True)
print(f"Found {len(files)} monthly files to process")

# Read and combine them
dfs = [pd.read_excel(f) for f in files]
df = pd.concat(dfs)

# Aggregate counts for each (Patient Harm, Brand Name, Manufacturer Name)
agg = df.groupby(['Patient Harm', 'Brand Name', 'Manufacturer Name'], as_index=False)['Count'].sum()

# Save to a new Excel file
agg.to_excel('harm_brand_manufacturer_one_year.xlsx', index=False)
print('Combined yearly Excel file created: harm_brand_manufacturer_one_year.xlsx')
