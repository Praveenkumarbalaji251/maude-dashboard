import pandas as pd

# Read the patient problem counts Excel file
try:
    df_patient = pd.read_excel('patient_problem_counts.xlsx')
    print("\nTop 50 patient problems from Excel file:")
    for idx, row in df_patient.head(50).iterrows():
        print(f"{row['Patient Problem']}: {row['Count']}")
except Exception as e:
    print(f"Error reading patient_problem_counts.xlsx: {e}")
