import pandas as pd
import ast

# The MAUDE CSV file is large, so we'll read only the first 10 rows
csv_path = 'maude_AUG2024_JULY2025.csv'

# Read first 10 rows
try:
    df = pd.read_csv(csv_path, nrows=10, low_memory=False)
    print(df.head(10))
except Exception as e:
    print(f"Error reading {csv_path}: {e}")
