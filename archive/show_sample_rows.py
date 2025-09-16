import pandas as pd
import ast

import calendar
from collections import Counter, defaultdict
from datetime import datetime


# --- Patient Problems Aggregation ---
# --- Patient Problems Aggregation ---
def extract_patient_problems(patient_str):
	try:
		patient_data = ast.literal_eval(patient_str)
		problems = []
		if isinstance(patient_data, list):
			for entry in patient_data:
				if isinstance(entry, dict) and 'patient_problems' in entry:
					problems.extend(entry['patient_problems'])
		return problems
	except Exception:
		return []
			try:
				strval = str(val)
				# Handle YYYYMMDD format
				if len(strval) == 8 and strval.isdigit():
					month = int(strval[4:6])
					if 1 <= month <= 12:
						return calendar.month_name[month]
				# Handle YYYY-MM-DD format
				elif len(strval) >= 10 and strval[4] == '-' and strval[7] == '-':
					month = int(strval[5:7])
					if 1 <= month <= 12:
						return calendar.month_name[month]
			except Exception:
				continue
	return 'Unknown'



def print_top_50_patient_problems_before_mapping(data):
	if 'patient' in data.columns:
		all_problems = []
		for patient_str in data['patient'].dropna():
			all_problems.extend(extract_patient_problems(patient_str))
		counter = Counter(all_problems)
		exclude = {'No Clinical Signs, Symptoms or Conditions', 'Insufficient Information'}
		filtered = {problem: count for problem, count in counter.items() if problem not in exclude}





def extract_event_month(row):
	for col in ['date_received', 'date_of_event']:
		val = row.get(col)
		if pd.notnull(val):
			strval = str(val)
			for fmt in ("%Y%m%d", "%Y-%m-%d", "%m/%d/%Y"):
				try:
					dt = datetime.strptime(strval, fmt)
					return dt.strftime("%Y-%m")
				except Exception:
					continue

	from collections import defaultdict

				except Exception:
		harm_map = defaultdict(int)
		if 'patient' in data.columns:
			for idx, row in data.iterrows():
				patient_str = row.get('patient')
				brand_name = None
				manufacturer_d_name = None
				event_month = extract_event_month(row)
				if event_month is None:
					continue
				if patient_str:
					try:
						patient_data = ast.literal_eval(patient_str)
						if isinstance(patient_data, list):
							for entry in patient_data:
								if isinstance(entry, dict):
									harms = entry.get('patient_problems', [])
									brand_name = entry.get('brand_name', None)
									manufacturer_d_name = entry.get('manufacturer_d_name', None)
									for harm in harms:
										key = (harm, brand_name, manufacturer_d_name, event_month)
										harm_map[key] += 1
					except Exception:
						continue
		return harm_map
					continue
# --- Patient Problems Aggregation ---
def aggregate_patient_problems(data):
	if 'patient' in data.columns:
		all_problems = []
		for patient_str in data['patient'].dropna():
			all_problems.extend(extract_patient_problems(patient_str))
		counter = Counter(all_problems)
		exclude = {'No Clinical Signs, Symptoms or Conditions', 'Insufficient Information'}
		filtered = {problem: count for problem, count in counter.items() if problem not in exclude}
		print("\nAggregated patient problems (descending order):")
		sorted_filtered = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
		for problem, count in sorted_filtered[:50]:
			print(f"{problem}: {count}")
		# Save to Excel
		df = pd.DataFrame(sorted_filtered, columns=['Patient Problem', 'Count'])
		df.to_excel('patient_problem_counts.xlsx', index=False)
		print("\nSaved to patient_problem_counts.xlsx")
	else:
		print("'patient' column not found in the data.")

import os
CSV_PATH = 'maude_AUG2024_JULY2025.csv'
if not os.path.exists(CSV_PATH):
	raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")
data = pd.read_csv(CSV_PATH)

	# Display the loaded rows
	print(data)

	# Print the list of columns
	print("\nColumns present in the data:")
	print(list(data.columns))

	# aggregate_patient_problems(data)  # Removed: function not defined
	print_top_50_patient_problems()
	print_top_50_patient_problems_before_mapping(data)
	df_harm = map_patient_harm_brand_manufacturer_month(data)
	# Save or use df_harm as needed
	# aggregate_product_problems(data)  # Only call if function is defined

	# ...existing code...
	sorted_filtered = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
	for problem, count in sorted_filtered:
		print(f"{problem}: {count}")
	# Save to Excel
	df = pd.DataFrame(sorted_filtered, columns=['Patient Problem', 'Count'])
	df.to_excel('patient_problem_counts.xlsx', index=False)
	print("\nSaved to patient_problem_counts.xlsx")
else:
	print("'patient' column not found in the data.")


print_top_50_patient_problems()


# --- Patient Problems Aggregation ---
def aggregate_patient_problems(data):
	if 'patient' in data.columns:
		all_problems = []
		for patient_str in data['patient'].dropna():
			all_problems.extend(extract_patient_problems(patient_str))
		counter = Counter(all_problems)
		exclude = {'No Clinical Signs, Symptoms or Conditions', 'Insufficient Information'}
		filtered = {problem: count for problem, count in counter.items() if problem not in exclude}
		print("\nAggregated patient problems (descending order):")
		sorted_filtered = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
		for problem, count in sorted_filtered[:50]:
			print(f"{problem}: {count}")




	harm_map = defaultdict(int)
	results = []
	if 'patient' in data.columns:
		for idx, row in data.iterrows():
			patient_str = row.get('patient')
			brand_name = None
			manufacturer_d_name = None
			event_month = extract_event_month(row)
			if patient_str:
				try:
					patient_data = ast.literal_eval(patient_str)
					if isinstance(patient_data, list):
						for entry in patient_data:
							if isinstance(entry, dict):
								harms = entry.get('patient_problems', [])
								brand_name = entry.get('brand_name', None)
								manufacturer_d_name = entry.get('manufacturer_d_name', None)
								for harm in harms:
									key = (harm, brand_name, manufacturer_d_name, event_month)
									harm_map[key] += 1
				except Exception:
					continue
		for (harm, brand, manufacturer, month), count in harm_map.items():
			results.append({
				'Patient Harm': harm,
				'Brand Name': brand,
				'Manufacturer Name': manufacturer,
				'Month': month,
				'Count': count
			})



