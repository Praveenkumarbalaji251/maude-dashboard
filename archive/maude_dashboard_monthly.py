import streamlit as st
import pandas as pd
import glob
import altair as alt

st.set_page_config(page_title="MAUDE Harm-Device-Manufacturer Dashboard", layout="wide")
st.title("MAUDE Harm-Device-Manufacturer Dashboard (Month-wise)")

# Find all harm-brand-manufacturer monthly Excel files
excel_files = sorted(glob.glob("harm_brand_manufacturer_*.xlsx"))

month_map = {}
for f in excel_files:
    base = f.replace("harm_brand_manufacturer_","").replace(".xlsx","")
    parts = base.split('_')
    if len(parts) == 2:
        # Ensure month is always three-letter capitalized (e.g., Aug, Sep)
        month_abbr = parts[0][:3].capitalize()
        year = parts[1]
        month_label = f"{month_abbr} {year}"
    else:
        month_label = base.title()
    # Only add if not already present
    if month_label not in month_map:
        month_map[month_label] = f


# Sidebar filters
st.sidebar.header("Filters")
# Sort months chronologically
def month_sort_key(label):
    parts = label.split()
    if len(parts) == 2:
        month_abbr = parts[0][:3].capitalize()
        year = int(parts[1])
        month_num = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(month_abbr) + 1
        return (year, month_num)
    return (9999, 99)
month_options = sorted(month_map.keys(), key=month_sort_key)
selected_month = st.sidebar.selectbox("Select Month-Year", options=month_options, index=0)
data_path = month_map[selected_month]
df = pd.read_excel(data_path)

selected_harm = st.sidebar.multiselect(
    "Select Patient Harm(s)", options=sorted(df["Patient Harm"].unique()), default=[])
selected_brand = st.sidebar.multiselect(
    "Select Brand Name(s)", options=sorted(df["Brand Name"].dropna().unique()), default=[])
selected_manufacturer = st.sidebar.multiselect(
    "Select Manufacturer Name(s)", options=sorted(df["Manufacturer Name"].dropna().unique()), default=[])

filtered_df = df.copy()
if selected_harm:
    filtered_df = filtered_df[filtered_df["Patient Harm"].isin(selected_harm)]
if selected_brand:
    filtered_df = filtered_df[filtered_df["Brand Name"].isin(selected_brand)]
if selected_manufacturer:
    filtered_df = filtered_df[filtered_df["Manufacturer Name"].isin(selected_manufacturer)]

st.subheader(f"Aggregated Harm Counts by Device and Manufacturer for {selected_month}")
st.dataframe(filtered_df, width='stretch')

st.subheader("Top Harms by Device and Manufacturer")
top_n = st.slider("Show Top N", min_value=5, max_value=50, value=20)
top_df = filtered_df.sort_values("Count", ascending=False).head(top_n)
if not top_df.empty:
    chart = alt.Chart(top_df).mark_bar().encode(
        x=alt.X('Patient Harm:N', sort='-y'),
        y='Count:Q',
        color='Brand Name:N',
        tooltip=['Patient Harm', 'Brand Name', 'Manufacturer Name', 'Count']
    ).properties(width=900, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data to display for selected filters.")


# Second visualization: Patient Problem Total Counts
st.subheader("Total Patient Problem Counts (All Months)")
try:
    df_patient = pd.read_excel("patient_problem_counts.xlsx")
    df_patient_sorted = df_patient.sort_values("Count", ascending=False)
    chart_patient = alt.Chart(df_patient_sorted).mark_bar().encode(
        x=alt.X('Patient Problem:N', sort='-y'),
        y='Count:Q',
        tooltip=['Patient Problem', 'Count']
    ).properties(width=900, height=400)
    st.altair_chart(chart_patient, use_container_width=True)
    st.dataframe(df_patient_sorted, width='stretch')
except Exception as e:
    st.warning(f"Could not load patient_problem_counts.xlsx: {e}")


