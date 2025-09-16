import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MAUDE Death Cases Dashboard", layout="wide")
st.title("MAUDE Death Cases Dashboard")

data_path = "death_product_problem_by_device_desc.xlsx"
try:
    df = pd.read_excel(data_path)
except FileNotFoundError:
    st.error(f"Data file not found: {data_path}")
    st.stop()
except Exception as e:
    st.error(f"Error reading data file: {e}")
    st.stop()

st.sidebar.header("Filters")
selected_problem = st.sidebar.multiselect(
    "Select Product Problem(s)", options=sorted(df["Product Problem"].dropna().unique()), default=[])
selected_brand = st.sidebar.multiselect(
    "Select Brand Name(s)", options=sorted(df["Brand Name"].dropna().unique()), default=[])
selected_manufacturer = st.sidebar.multiselect(
    "Select Manufacturer Name(s)", options=sorted(df["Manufacturer Name"].dropna().unique()), default=[])

filtered_df = df.copy()
if selected_problem:
    filtered_df = filtered_df[filtered_df["Product Problem"].isin(selected_problem)]
if selected_brand:
    filtered_df = filtered_df[filtered_df["Brand Name"].isin(selected_brand)]
if selected_manufacturer:
    filtered_df = filtered_df[filtered_df["Manufacturer Name"].isin(selected_manufacturer)]

sort_desc = st.sidebar.checkbox("Sort by Death Count (Descending)", value=True)
if sort_desc:
    filtered_df = filtered_df.sort_values("Death Count", ascending=False)
else:
    filtered_df = filtered_df.sort_values("Death Count", ascending=True)

st.subheader("Death Cases by Product Problem, Device, and Manufacturer")
st.dataframe(filtered_df, width='stretch')

st.subheader("Top Death Counts by Product Problem")
top_n = st.slider("Show Top N", min_value=5, max_value=50, value=20)
top_df = filtered_df.sort_values("Death Count", ascending=False).head(top_n)
if not top_df.empty:
    chart = alt.Chart(top_df).mark_bar().encode(
        x=alt.X('Product Problem:N', sort='-y'),
        y='Death Count:Q',
        color='Brand Name:N',
        tooltip=['Product Problem', 'Brand Name', 'Manufacturer Name', 'Death Count']
    ).properties(width=900, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data to display for selected filters.")

st.caption(f"Data source: {data_path}")
