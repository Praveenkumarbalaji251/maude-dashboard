import pandas as pd
import numpy as np

def create_device_summary(df):
    # Group by device and count deaths
    device_summary = df['Brand Name'].value_counts().reset_index()
    device_summary.columns = ['Device Name', 'Death Count']
    
    # Pre-compute problems for all devices efficiently
    def get_all_device_problems(problem_column, top_n=5):
        device_problems = {}
        grouped = df.groupby('Brand Name')[problem_column].apply(
            lambda x: '; '.join(x.dropna())
        )
        for device_name, problems_str in grouped.items():
            if problems_str:
                problems = problems_str.split('; ')
                device_problems[device_name] = pd.Series(problems).value_counts().head(top_n).to_dict()
            else:
                device_problems[device_name] = {}
        return device_problems
    patient_problems_dict = get_all_device_problems('Patient Problems')
    product_problems_dict = get_all_device_problems('Product Problems')
    
    device_summary['Top Patient Problems'] = device_summary['Device Name'].map(
        lambda x: str(patient_problems_dict.get(x, {})))
    device_summary['Top Product Problems'] = device_summary['Device Name'].map(
        lambda x: str(product_problems_dict.get(x, {})))
    
    return device_summary

def create_problem_summary(df, problem_column):
    # Extract all problems from the specified column
    all_problems = []
    for _, row in df.iterrows():
        if pd.notna(row[problem_column]):
            problems = row[problem_column].split('; ')
            all_problems.extend(problems)
    
    # Create summary with counts
    problem_summary = pd.Series(all_problems).value_counts().reset_index()
    problem_summary.columns = ['Problem', 'Count']
    return problem_summary
def create_device_problem_matrix(df, problem_column):
    # Create expanded DataFrame with one row per device-problem combination
    expanded_data = []
    for _, row in df.iterrows():
        device = row['Brand Name']
        if pd.notna(row[problem_column]):
            problems = row[problem_column].split('; ')
            for problem in problems:
                expanded_data.append({'Device': device, 'Problem': problem})

    if not expanded_data:
        return pd.DataFrame()

    expanded_df = pd.DataFrame(expanded_data)
    return expanded_df
            problems = row[problem_column].split('; ')
            for problem in problems:
                expanded_data.append({'Device': device, 'Problem': problem})

    if not expanded_data:
        return pd.DataFrame()

    expanded_df = pd.DataFrame(expanded_data)
def main():
    try:
        # Read the data
        print("Reading data...")
        df = pd.read_excel('death_cases_510k_devices_with_problems.xlsx')
        
        # Validate required columns exist
        required_columns = ['Brand Name', 'Patient Problems', 'Product Problems']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Validate data is not empty
        if df.empty:
            raise ValueError("Input file is empty")
            
        print(f"Loaded {len(df)} records with {df['Brand Name'].nunique()} unique devices")

        # Create Excel writer
        print("Creating Excel workbook...")
        with pd.ExcelWriter('510k_death_analysis_summary.xlsx', engine='openpyxl') as writer:
            # 1. Overview sheet
            overview = pd.DataFrame({
                'Metric': [
                    'Total Death Cases',
                    'Unique Devices',
                    'Total Patient Problems',
                    'Total Product Problems'
                ],
                'Value': [
                    len(df),
                    df['Brand Name'].nunique(),
                    df['Patient Problems'].str.split('; ').explode().nunique(),
                    df['Product Problems'].str.split('; ').explode().nunique()
                ]
            })
            overview.to_excel(writer, sheet_name='Overview', index=False)
            
            # 2. Device Summary
            print("Creating device summary...")
            device_summary = create_device_summary(df)
            device_summary.to_excel(writer, sheet_name='Device Summary', index=False)
            
            # 3. Patient Problems Summary
            print("Creating patient problems summary...")
            patient_problems = create_problem_summary(df, 'Patient Problems')
            patient_problems.to_excel(writer, sheet_name='Patient Problems', index=False)
            
            # 4. Product Problems Summary
            print("Creating product problems summary...")
            product_problems = create_problem_summary(df, 'Product Problems')
            product_problems.to_excel(writer, sheet_name='Product Problems', index=False)
            
            # 5. Device-Patient Problem Matrix
            print("Creating device-patient problem matrix...")
            patient_matrix = create_device_problem_matrix(df, 'Patient Problems')
            patient_matrix.to_excel(writer, sheet_name='Device-Patient Matrix')
            
            # 6. Device-Product Problem Matrix
            print("Creating device-product problem matrix...")
            product_matrix = create_device_problem_matrix(df, 'Product Problems')
            product_matrix.to_excel(writer, sheet_name='Device-Product Matrix')
            
            # 7. Top 20 Devices Detail
            print("Creating detailed analysis for top devices...")
            top_devices = df['Brand Name'].value_counts().head(20).index

    
    print("\nAnalysis complete! File saved as '510k_death_analysis_summary.xlsx'")
    print("\nWorkbook contains the following sheets:")
    print("1. Overview - Key statistics")
    print("2. Device Summary - List of all devices with death counts and top problems")
    print("3. Patient Problems - All patient problems ranked by frequency")
    print("4. Product Problems - All product problems ranked by frequency")
    print("5. Device-Patient Matrix - Matrix of devices vs patient problems")
    print("6. Device-Product Matrix - Matrix of devices vs product problems")
    print("7. Top 20 Devices Detail - Detailed records for top 20 devices by death count")

if __name__ == "__main__":
    main()
