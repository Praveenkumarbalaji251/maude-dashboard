import pandas as pd

# Read the analysis results
try:
    df = pd.read_excel('death_cases_510k_devices_with_problems.xlsx')
except FileNotFoundError:
    print("Error: Excel file 'death_cases_510k_devices_with_problems.xlsx' not found.")
    exit(1)
def analyze_problems(device_df, problem_column, problem_type):
    """Extract and count problems for a specific device and problem type."""
    problems = []
    for problem_text in device_df[problem_column].dropna():
        problems.extend(problem_text.split('; '))
    
    if problems:
        problem_counts = pd.Series(problems).value_counts()
        print(f"\nTop {problem_type} Problems:")
        for problem, count in problem_counts.head(5).items():
            print(f"- {problem}: {count} cases")

death_counts = df['Brand Name'].value_counts()

print("\n=== Devices with Most Death Reports ===")
print("-" * 80)
for brand, count in death_counts.head(10).items():
    # Filter once per device
    device_df = df[df['Brand Name'] == brand]
    
    print(f"\nDevice: {brand}")
    print(f"Death Count: {count}")
    
    analyze_problems(device_df, 'Patient Problems', 'Patient')
    analyze_problems(device_df, 'Product Problems', 'Product')
    
    print("-" * 80)
    if device_product_problems:
        problem_counts = pd.Series(device_product_problems).value_counts()
        print("\nTop Product Problems:")
        for problem, prob_count in problem_counts.head(5).items():
            print(f"- {problem}: {prob_count} cases")
    
    print("-" * 80)

# Overall statistics
print("\n=== Overall Statistics ===")
print(f"Total number of death cases: {len(df)}")
print(f"Number of unique devices: {len(death_counts)}")

# Most common patient problems overall
print("\n=== Most Common Patient Problems Overall ===")
all_patient_problems = []
for problems in df['Patient Problems'].dropna():
    all_patient_problems.extend(problems.split('; '))
if all_patient_problems:
    problem_counts = pd.Series(all_patient_problems).value_counts()
    for problem, count in problem_counts.head(10).items():
        print(f"{problem}: {count} cases")

# Most common product problems overall
print("\n=== Most Common Product Problems Overall ===")
all_product_problems = []
for problems in df['Product Problems'].dropna():
    all_product_problems.extend(problems.split('; '))
if all_product_problems:
    problem_counts = pd.Series(all_product_problems).value_counts()
    for problem, count in problem_counts.head(10).items():
        print(f"{problem}: {count} cases")
