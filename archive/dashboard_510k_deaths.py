import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Device Deaths: Patient & Product Problems", layout="wide")
st.title("Device Deaths: Patient & Product Problem Associations Dashboard")

# Load the detailed analysis data
@st.cache_data
def load_data():
    df = pd.read_excel('device_death_patient_product_problems.xlsx')
    # Convert columns to string and handle NaN values
    for col in ['Device Name', 'Patient Problem', 'Product Problems']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str)
    return df


try:
    df = load_data()
    st.sidebar.header("Filters")
    # Device filter
    device_names = ['All'] + sorted(df['Device Name'].unique())
    selected_device = st.sidebar.selectbox('Select Device:', device_names)
    # Patient Problem filter
    patient_problems = ['All'] + sorted(df['Patient Problem'].unique())
    selected_patient_problem = st.sidebar.selectbox('Select Patient Problem:', patient_problems)
    # Product Problem filter
    all_product_problems = set()
    for problems in df['Product Problems']:
        all_product_problems.update([p.strip() for p in problems.split(';') if p.strip()])
    product_problems = ['All'] + sorted(all_product_problems)
    selected_product_problem = st.sidebar.selectbox('Select Product Problem:', product_problems)

    # Apply filters
    filtered_df = df.copy()
    if selected_device != 'All':
        filtered_df = filtered_df[filtered_df['Device Name'] == selected_device]
    if selected_patient_problem != 'All':
        filtered_df = filtered_df[filtered_df['Patient Problem'] == selected_patient_problem]
    if selected_product_problem != 'All':
        filtered_df = filtered_df[filtered_df['Product Problems'].str.contains(selected_product_problem)]

    # Overview metrics
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Death Cases", filtered_df['Death Count'].sum())
    with col2:
        st.metric("Unique Devices", filtered_df['Device Name'].nunique())
    with col3:
        st.metric("Unique Patient Problems", filtered_df['Patient Problem'].nunique())

    # Bar chart: Deaths by Device
    st.subheader("Deaths by Device")
    top_devices = filtered_df.groupby('Device Name')['Death Count'].max().sort_values(ascending=False).head(20)
    fig_devices = px.bar(
        x=top_devices.index,
        y=top_devices.values,
        title="Top Devices by Death Count",
        labels={'x': 'Device Name', 'y': 'Death Count'}
    )
    fig_devices.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_devices, use_container_width=True)

    # Table: Patient Problem and Product Problem associations
    st.subheader("Patient Problem & Product Problem Associations")
    st.dataframe(filtered_df[['Device Name', 'Death Count', 'Patient Problem', 'Problem Occurrences', 'Product Problems']], use_container_width=True)

    # Download filtered data
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name="filtered_device_patient_product_problems.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("Please run the analysis script to generate 'device_death_patient_product_problems.xlsx'.")
    st.info("Run: python analyze_deaths_detailed.py")
