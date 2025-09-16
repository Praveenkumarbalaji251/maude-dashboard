import pandas as pd

# Load the mapping Excel file
file_path = 'brand_patient_manufacturer_month_1000.xlsx'
df = pd.read_excel(file_path)

# Print the first 10 rows to the chat
print(df.head(10))
