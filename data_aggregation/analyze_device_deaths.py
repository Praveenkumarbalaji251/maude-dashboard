import pandas as pd

# Read the data
df = pd.read_excel('death_cases_510k_devices_with_problems.xlsx')

# Function to extract unique problems from semicolon-separated string
def get_unique_problems(problems_series):
    all_problems = []
    for problems in problems_series.dropna():
        problems_list = [p.strip() for p in problems.split(';')]
        all_problems.extend(problems_list)
    return list(set(all_problems))

# Group by Brand Name and get death counts and patient problems
device_analysis = df.groupby(['Brand Name']).agg({
    'K Number': 'count',  # Count of death cases
    'Patient Problems': get_unique_problems  # Unique patient problems
}).reset_index()

# Rename columns for clarity
device_analysis.columns = ['Device Name', 'Death Count', 'Patient Problems']

# Sort by death count in descending order
device_analysis = device_analysis.sort_values('Death Count', ascending=False)

# Sort by death count in descending order
device_analysis = device_analysis.sort_values('Death Count', ascending=False)

# Print the results
print("\n=== Device Death Analysis ===\n")
for _, row in device_analysis.iterrows():
    print(f"Device: {row['Device Name']}")
    print(f"Death Count: {row['Death Count']}")
    print("Patient Problems:")
    if row['Patient Problems']:
        for problem in sorted(row['Patient Problems']):
            print(f"  - {problem}")
    else:
        print("  No patient problems recorded")
    print("\n" + "-"*50 + "\n")

# Save to Excel for further analysis
device_analysis.to_excel('device_death_patient_problems.xlsx', index=False)
print("\nAnalysis has been saved to 'device_death_patient_problems.xlsx'")
