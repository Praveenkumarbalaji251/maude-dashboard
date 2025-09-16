# --- IMPORTS ---
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import io
import os
import re
import glob
import calendar

# --- TOP SECTIONS: Aggregated Harm Counts Table & Top Harms Chart ---
st.set_page_config(page_title="MAUDE Harm-Device-Manufacturer Dashboard", layout="wide")
st.title("MAUDE Harm-Device-Manufacturer Dashboard")

# Find all harm-brand-manufacturer monthly Excel files with robust validation
excel_files = sorted(glob.glob("data/processed/harm_brand_manufacturer_*.xlsx"))
yearly_summary_path = "data/processed/harm_brand_harm_descending.xlsx"
if not excel_files:
    st.error("No harm-brand-manufacturer Excel files found. Please check your data directory.")
    st.stop()
month_map = {}
exclude_pattern = re.compile(r"one[_-]?year|death[_-]?cases", re.IGNORECASE)
month_file_pattern = re.compile(r"harm_brand_manufacturer_([a-zA-Z]+)_?(\d{4})?\.xlsx", re.IGNORECASE)

for f in excel_files:
    # Exclude files matching summary/death patterns or not matching month-year pattern
    if exclude_pattern.search(f):
        continue
    if not os.path.isfile(f) or not os.access(f, os.R_OK):
        st.warning(f"File not found or not readable, skipping: {f}")
        continue
    # Extract just the filename for label
    filename = os.path.basename(f)
    base = filename.replace("harm_brand_manufacturer_", "").replace(".xlsx", "")
    # Expecting base like 'Apr_2025' or 'Aug_2024', etc.
    parts = base.split('_')
    if len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit():
        # Capitalize first 3 letters for month, keep year as is
        month = parts[0][:3].capitalize()
        year = parts[1]
        month_label = f"{month} {year}"
        month_map[month_label] = f
    else:
        # Only add if it looks like a valid month label
        if not month_file_pattern.match(filename):
            st.warning(f"Skipping file with unexpected pattern: {filename}")
            continue
        # Fallback: use cleaned base
        month_label = base.replace('_', ' ').title()
        month_map[month_label] = f

# Add a 'Yearly Summary' option if the file exists
if os.path.isfile(yearly_summary_path) and os.access(yearly_summary_path, os.R_OK):
    month_map["Yearly Summary"] = yearly_summary_path
else:
    st.warning(f"Yearly summary file not found: {yearly_summary_path}. 'Yearly Summary' option will not be available.")

st.sidebar.header("Filters")

selected_month = st.sidebar.selectbox("Select Month-Year", options=list(month_map.keys()), index=0)
data_path = month_map[selected_month]

@st.cache_data
def load_excel_data(file_path):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        st.stop()

df = load_excel_data(data_path)


# Add a sort toggle for descending/ascending order (only once, with unique key)
sort_desc = st.sidebar.checkbox("Sort by Count (Descending)", value=True, key="sort_desc_checkbox")




def plot_schwabish_bar(data, title, subtitle, xlabel):
    top_harms = data.groupby('Patient Harm')['Count'].sum().sort_values(ascending=False).head(15)
    total_harms = data['Count'].sum()
    percentages = (top_harms / total_harms * 100).round(1)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#E41A1C'] + ['#377EB8'] * (len(top_harms) - 1)
    bars = ax.barh(range(len(top_harms)), top_harms, color=colors)
    for i, (count, percentage) in enumerate(zip(top_harms, percentages)):
        ax.text(count + 10, i, f'{count:,}', va='center', ha='left', fontsize=10)
        if count > 100:
            ax.text(count/2, i, f'{percentage}%', va='center', ha='center', color='white', fontsize=10, fontweight='bold')
    ax.set_yticks(range(len(top_harms)))
    ax.set_yticklabels(top_harms.index, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.suptitle(title, x=0.01, ha='left', y=0.98, fontsize=14, fontweight='bold')
    plt.title(subtitle, x=0.01, ha='left', pad=10, fontsize=11, style='italic')
    plt.figtext(0.01, 0.02, 'Data source: MAUDE | Analysis: Schwabish principles', ha='left', fontsize=8, style='italic')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, bottom=0.1, top=0.9)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


if selected_month == "Yearly Summary":
    st.subheader("Yearly Aggregated Harm Counts by Device and Manufacturer")
    # Only show sorted table, no filters
    if sort_desc:
        df = df.sort_values("Count", ascending=False)
    else:
        df = df.sort_values("Count", ascending=True)
    st.dataframe(df, width='stretch')
    st.subheader("Top Harms by Device and Manufacturer")
    top_n = st.slider("Show Top N", min_value=5, max_value=50, value=20)
    top_df = df.sort_values("Count", ascending=False).head(top_n)
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
    st.caption(f"Data source: {data_path}")
    if st.button("Show Schwabish Bar Chart (Top 15 Harms)"):
        subtitle = f'Top 15 harms account for {(df.head(15)["Count"].sum() / df["Count"].sum() * 100):.1f}% of {df["Count"].sum():,} total incidents'
        buf = plot_schwabish_bar(df, 'Top Patient Harms (Yearly MAUDE Summary)', subtitle, 'Number of Harm Incidents')
        st.image(buf)
else:
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
    if sort_desc:
        filtered_df = filtered_df.sort_values("Count", ascending=False)
    else:
        filtered_df = filtered_df.sort_values("Count", ascending=True)
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
    st.caption(f"Data source: {data_path}")
    if st.button("Show Schwabish Bar Chart (Top 15 Harms)"):
        subtitle = f'Top 15 harms account for {(filtered_df.head(15)["Count"].sum() / filtered_df["Count"].sum() * 100):.1f}% of {filtered_df["Count"].sum():,} total incidents'
        buf = plot_schwabish_bar(filtered_df, f'Top Patient Harms in {selected_month} (MAUDE)', subtitle, 'Number of Harm Incidents')
        st.image(buf)

# --- Timeline Chart: Trend of Total Harm Incidents Over Time ---


# Aggregate all months for timeline
timeline_files = sorted(glob.glob("data/processed/harm_brand_manufacturer_*.xlsx"))
timeline_data = []
for f in timeline_files:
    filename = os.path.basename(f)
    base = filename.replace("harm_brand_manufacturer_","").replace(".xlsx","")
    parts = base.split('_')
    if len(parts) == 2 and parts[1].isdigit():
        month = parts[0].capitalize()
        year = parts[1]
        month_label = f"{month} {year}"
    else:
        continue
    try:
        df_month = pd.read_excel(f)
        total_count = df_month['Count'].sum()
        timeline_data.append({"Month": month_label, "Total Incidents": total_count})
    except Exception:
        continue
timeline_df = pd.DataFrame(timeline_data)
if not timeline_df.empty:
    timeline_df['Month'] = pd.Categorical(timeline_df['Month'], categories=sorted(timeline_df['Month'], key=lambda x: (int(x.split()[1]), list(calendar.month_abbr).index(x.split()[0][:3]))), ordered=True)
    timeline_df = timeline_df.sort_values('Month')
    st.subheader("Timeline: Total Harm Incidents per Month")
    timeline_chart = alt.Chart(timeline_df).mark_line(point=True).encode(
        x=alt.X('Month:N', sort=list(timeline_df['Month'])),
        y='Total Incidents:Q',
        tooltip=['Month', 'Total Incidents']
    ).properties(width=900, height=350)
    st.altair_chart(timeline_chart, use_container_width=True)
