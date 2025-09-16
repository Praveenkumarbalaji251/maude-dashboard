import pandas as pd
import ast
import calendar

# Load the patient harm Excel file
file_path = 'patient_harm_brand_manufacturer_month_test.xlsx'
df = pd.read_excel(file_path)

# Prepare new columns for brand name, manufacturer name, month, and year
brand_names = []
manufacturer_names = []
months = []
years = []

for idx, row in df.iterrows():
    # Extract brand name from device nested (if available)
    brand_name = row.get('Brand Name')
    if pd.isnull(brand_name):
        brand_name = None
    brand_names.append(brand_name)

    # Extract manufacturer name from 'manufacturer_g1_name' column (if available)
    manufacturer_name = row.get('Manufacturer Name')
    if pd.isnull(manufacturer_name):
        manufacturer_name = None
    manufacturer_names.append(manufacturer_name)

    # Extract month and year from 'Month' column
    month_year = row.get('Month')
    if pd.isnull(month_year):
        months.append(None)
        years.append(None)
    else:
        # If month_year is like 'August 2024', split
        parts = str(month_year).split()
        if len(parts) == 2 and parts[1].isdigit():
            months.append(parts[0])
            years.append(parts[1])
        else:
            months.append(month_year)
            years.append(None)

# Add new columns to DataFrame
df['Extracted Brand Name'] = brand_names
df['Extracted Manufacturer Name'] = manufacturer_names
df['Extracted Month'] = months
df['Extracted Year'] = years

# Save the updated DataFrame to a new Excel file
output_path = 'patient_harm_brand_manufacturer_month_extracted.xlsx'
df.to_excel(output_path, index=False)
print(f"Saved extracted mapping to {output_path}")
