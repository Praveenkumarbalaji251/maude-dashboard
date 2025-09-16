import pandas as pd
import json

# Read the data
import sys

try:
    df = pd.read_excel('death_cases_510k_devices_with_problems.xlsx')
except FileNotFoundError:
    print("Error: Input file 'death_cases_510k_devices_with_problems.xlsx' not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    sys.exit(1)
# Function to extract unique problems from semicolon-separated string
def get_unique_problems(problems_series):
    all_problems = []
    for problems in problems_series.dropna():
        problems_list = [p.strip() for p in problems.split(';')]
        all_problems.extend(problems_list)
    return sorted(list(set(all_problems)))

# Function to create problem-product mapping
def analyze_device_problems(device_data):
    problem_map = {}
    
    for _, row in device_data.iterrows():
        patient_problems = row['Patient Problems'].split(';') if pd.notna(row['Patient Problems']) else []
        product_problems = row['Product Problems'].split(';') if pd.notna(row['Product Problems']) else []
        
        for pp in patient_problems:
            pp = pp.strip()
            if pp not in problem_map:
                problem_map[pp] = {'count': 0, 'product_problems': set()}
            
            problem_map[pp]['count'] += 1
            for prod in product_problems:
                if pd.notna(prod) and prod.strip():
# Group by Brand Name and analyze problems
device_analysis = df.groupby(['Brand Name']).agg({
    'K Number': 'count',  # Count of death cases
    'Patient Problems': get_unique_problems,  # Unique patient problems
}).reset_index()

# Add problem analysis
device_analysis['Problem_Analysis'] = df.groupby(['Brand Name']).apply(analyze_device_problems)
device_analysis = df.groupby(['Brand Name']).agg({
    'K Number': 'count',  # Count of death cases
    'Patient Problems': get_unique_problems,  # Unique patient problems
}).reset_index()

# Add problem analysis
device_analysis['Problem_Analysis'] = df.groupby(['Brand Name']).apply(analyze_device_problems)

# Rename columns for clarity
device_analysis.columns = ['Device Name', 'Death Count', 'Patient Problems', 'Problem_Analysis']

# Sort by death count in descending order
device_analysis = device_analysis.sort_values('Death Count', ascending=False)

# Calculate total deaths and percentages
total_deaths = device_analysis['Death Count'].sum()
top_10_deaths = device_analysis.head(10)['Death Count'].sum()

print("\n=== Device Death Analysis Summary ===")
print(f"Total Deaths Analyzed: {total_deaths}")
print(f"Top 10 Devices Account for: {top_10_deaths} deaths ({(top_10_deaths/total_deaths)*100:.1f}% of total)")
print("\n=== Top 10 Devices by Death Count ===\n")

# Print details for top 10 devices
for _, row in device_analysis.head(10).iterrows():
    print(f"Device: {row['Device Name']}")
    print(f"Death Count: {row['Death Count']} ({(row['Death Count']/total_deaths)*100:.1f}% of total deaths)")
    print("Patient Problems and Associated Product Problems:")
    
    if row['Patient Problems']:
        problem_analysis = json.loads(row['Problem_Analysis'])
        for problem in sorted(problem_analysis.keys()):
            print(f"\nPatient Problem: {problem}")
            print(f"Occurrences: {problem_analysis[problem]['count']}")
            if problem_analysis[problem]['product_problems']:
                print("Associated Product Problems:")
                for pp in problem_analysis[problem]['product_problems']:
                    print(f"  - {pp}")
            else:
                print("  No associated product problems recorded")
    else:
        print("  No patient problems recorded")
    print("\n" + "-"*50 + "\n")

# Save full analysis to Excel
device_analysis.to_excel('device_death_patient_product_problems.xlsx', index=False)
print("\nFull analysis has been saved to 'device_death_patient_product_problems.xlsx'")
