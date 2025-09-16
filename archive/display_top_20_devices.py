import pandas as pd
import tabulate

# Read the Excel file
try:
    df = pd.read_excel('510k_death_analysis_summary.xlsx', sheet_name='Device Summary')
except FileNotFoundError:
    print("Error: Could not find '510k_death_analysis_summary.xlsx' in current directory")
    exit(1)
except Exception as e:
# Clean up the problem columns for better display
top_20 = top_20.copy()  # Avoid SettingWithCopyWarning

def clean_text_column(text):
    if pd.isna(text):
        return ""
    return str(text).replace('{', '').replace('}', '').replace("'", "")

for col in ['Top Patient Problems', 'Top Product Problems']:
    if col in top_20.columns:
        top_20[col] = top_20[col].apply(clean_text_column)
    else:
        print(f"Warning: Column '{col}' not found in data")

# Get top 20 devices
top_20 = df.head(20)

# Clean up the problem columns for better display
top_20['Top Patient Problems'] = top_20['Top Patient Problems'].apply(lambda x: x.replace('{', '').replace('}', '').replace("'", ""))
top_20['Top Product Problems'] = top_20['Top Product Problems'].apply(lambda x: x.replace('{', '').replace('}', '').replace("'", ""))

# Format the table
print("\n=== Top 20 Devices by Death Count ===\n")
print(tabulate.tabulate(top_20, headers='keys', tablefmt='grid', showindex=False))

# Print some statistics
total_deaths = df['Death Count'].sum()
top_20_deaths = top_20['Death Count'].sum()
percentage = (top_20_deaths / total_deaths) * 100

print(f"\nSummary Statistics:")
print(f"Total deaths across all devices: {total_deaths}")
print(f"Deaths in top 20 devices: {top_20_deaths}")
print(f"Percentage of deaths in top 20 devices: {percentage:.2f}%")
