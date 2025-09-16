import pandas as pd

import sys

# Load the extracted mapping Excel file
file_path = sys.argv[1] if len(sys.argv) > 1 else 'patient_harm_brand_manufacturer_month_extracted.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit(1)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Print the first 10 rows to the chat
print(df.head(10))
