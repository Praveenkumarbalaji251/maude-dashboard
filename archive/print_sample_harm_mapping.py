import pandas as pd

# Read the mapping Excel file and print a few rows
try:
    df = pd.read_excel('patient_harm_brand_manufacturer_month_test.xlsx')
    print("\nSample rows from patient_harm_brand_manufacturer_month_test.xlsx:")
    print(df.head(10))
except Exception as e:
    print(f"Error reading patient_harm_brand_manufacturer_month_test.xlsx: {e}")
