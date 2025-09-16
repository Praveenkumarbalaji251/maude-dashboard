# Print the first 10 raw lines from the MAUDE CSV file
csv_path = 'maude_AUG2024_JULY2025.csv'

try:
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i in range(10):
            line = f.readline()
            print(line.strip())
except Exception as e:
    print(f"Error reading raw lines from {csv_path}: {e}")
