import pandas as pd
import sys
import logging

def main():
    # Read the data
    try:
        df = pd.read_excel('death_cases_510k_devices_with_problems.xlsx')
    except FileNotFoundError:
        logging.error("File 'death_cases_510k_devices_with_problems.xlsx' not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        sys.exit(1)

    # Function to extract unique problems from semicolon-separated string
    def get_unique_problems(problems_series):
        all_problems = []
        for problems in problems_series.dropna():
            problems_list = [p.strip() for p in problems.split(';')]
            all_problems.extend(problems_list)
        return sorted(list(set(all_problems)))

    # Function to analyze problems and their relationships
    def analyze_device_records(device_data):
        problem_analysis = {}
        for _, row in device_data.iterrows():
            if pd.notna(row['Patient Problems']):
                patient_problems = [p.strip() for p in row['Patient Problems'].split(';')]
                product_problems = []
                if pd.notna(row['Product Problems']):
                    product_problems = [p.strip() for p in row['Product Problems'].split(';')]
                for pp in patient_problems:
                    if pp not in problem_analysis:
                        problem_analysis[pp] = {'count': 0, 'product_problems': set()}
                    problem_analysis[pp]['count'] += 1
                    problem_analysis[pp]['product_problems'].update(p for p in product_problems if p)
        return problem_analysis

    # Group by Brand Name and get death counts and patient problems
    device_analysis = df.groupby(['Brand Name']).agg({
        'K Number': 'count',  # Count of death cases
        'Patient Problems': get_unique_problems  # Unique patient problems
    }).reset_index()

    # Add detailed problem analysis
    problem_analyses = {}
    for device in device_analysis['Brand Name']:
        device_data = df[df['Brand Name'] == device]
        problem_analyses[device] = analyze_device_records(device_data)

    # Rename columns for clarity
    device_analysis.columns = ['Device Name', 'Death Count', 'Patient Problems']

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
        device_name = row['Device Name']
        print(f"Device: {device_name}")
        print(f"Death Count: {row['Death Count']} ({(row['Death Count']/total_deaths)*100:.1f}% of total deaths)")
        print("Patient Problems and Associated Product Problems:")
        if row['Patient Problems']:
            device_problems = problem_analyses[device_name]
            for problem in sorted(device_problems.keys()):
                print(f"\nPatient Problem: {problem}")
                print(f"Occurrences: {device_problems[problem]['count']}")
                product_problems = sorted(device_problems[problem]['product_problems'])
                if product_problems:
                    print("Associated Product Problems:")
                    for pp in product_problems:
                        print(f"  - {pp}")
                else:
                    print("  No associated product problems recorded")
        else:
            print("  No patient problems recorded")
        print("\n" + "-"*50 + "\n")

    # Prepare data for Excel export
    excel_data = []
    for device_name in device_analysis['Device Name']:
        device_problems = problem_analyses[device_name]
        for problem, details in device_problems.items():
            excel_data.append({
                'Device Name': device_name,
                'Death Count': device_analysis[device_analysis['Device Name'] == device_name]['Death Count'].iloc[0],
                'Patient Problem': problem,
                'Problem Occurrences': details['count'],
                'Product Problems': '; '.join(sorted(details['product_problems'])) if details['product_problems'] else 'None'
            })

    # Save detailed analysis to Excel
    pd.DataFrame(excel_data).to_excel('device_death_patient_product_problems.xlsx', index=False)
    print("\nDetailed analysis has been saved to 'device_death_patient_product_problems.xlsx'")

# Function to extract unique problems from semicolon-separated string
def get_unique_problems(problems_series):
    all_problems = []
    for problems in problems_series.dropna():
        problems_list = [p.strip() for p in problems.split(';')]
        all_problems.extend(problems_list)
    return sorted(list(set(all_problems)))

# Function to analyze problems and their relationships
def analyze_device_records(device_data):
    problem_analysis = {}
    
    for _, row in device_data.iterrows():
        if pd.notna(row['Patient Problems']):
            patient_problems = [p.strip() for p in row['Patient Problems'].split(';')]
            product_problems = []
            if pd.notna(row['Product Problems']):
                product_problems = [p.strip() for p in row['Product Problems'].split(';')]
            
            for pp in patient_problems:
                if pp not in problem_analysis:
                    problem_analysis[pp] = {'count': 0, 'product_problems': set()}
                problem_analysis[pp]['count'] += 1
                problem_analysis[pp]['product_problems'].update(p for p in product_problems if p)
    
    return problem_analysis

# Group by Brand Name and get death counts and patient problems
device_analysis = df.groupby(['Brand Name']).agg({
    'K Number': 'count',  # Count of death cases
    'Patient Problems': get_unique_problems  # Unique patient problems
}).reset_index()

# Add detailed problem analysis
problem_analyses = {}
for device in device_analysis['Brand Name']:
    device_data = df[df['Brand Name'] == device]
    problem_analyses[device] = analyze_device_records(device_data)

# Rename columns for clarity
device_analysis.columns = ['Device Name', 'Death Count', 'Patient Problems']

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
    device_name = row['Device Name']
    print(f"Device: {device_name}")
    print(f"Death Count: {row['Death Count']} ({(row['Death Count']/total_deaths)*100:.1f}% of total deaths)")
    print("Patient Problems and Associated Product Problems:")
    
    if row['Patient Problems']:
        device_problems = problem_analyses[device_name]
        for problem in sorted(device_problems.keys()):
            print(f"\nPatient Problem: {problem}")
            print(f"Occurrences: {device_problems[problem]['count']}")
            product_problems = sorted(device_problems[problem]['product_problems'])
            if product_problems:
                print("Associated Product Problems:")
                for pp in product_problems:
                    print(f"  - {pp}")
            else:
                print("  No associated product problems recorded")
    else:
        print("  No patient problems recorded")
    print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()
