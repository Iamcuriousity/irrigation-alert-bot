
import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
rainfall_data = pd.read_excel('/mnt/data/rainfall data.xlsx')
evapotranspiration_data = pd.read_excel('/mnt/data/evapotransipitaion potential.xlsx')

# Merge datasets
merged_data = pd.merge(rainfall_data, evapotranspiration_data, on=['Dist Code', 'Year'])

# Filter for the latest year
latest_year = merged_data['Year'].max()
latest_year_data = merged_data[merged_data['Year'] == latest_year]

# Define alert generation function
def generate_irrigation_alert(row):
    rainfall_total = row['ANNUAL RAINFALL (Millimeters)']
    evapotranspiration_total = sum([
        row[col] for col in evapotranspiration_data.columns if 'POTENTIAL' in col
    ])
    water_balance = rainfall_total - evapotranspiration_total
    if water_balance < 50:
        return "⚠️ Under-watering Alert! Increase irrigation."
    elif water_balance > 100:
        return "⚠️ Over-watering Alert! Reduce irrigation."
    return "✅ Optimal Water Balance."

# Apply alert generation
latest_year_data['Irrigation Alert'] = latest_year_data.apply(generate_irrigation_alert, axis=1)

# Streamlit Dashboard
st.title(f"Irrigation Alert Dashboard for {latest_year}")
selected_district = st.selectbox("Select District:", latest_year_data['Dist Name_x'].unique())
filtered_data = latest_year_data[latest_year_data['Dist Name_x'] == selected_district]

# Display Data and Plot
st.write("### Water Balance Alerts for the Selected District")
st.dataframe(filtered_data[['Year', 'Irrigation Alert']])
fig = px.line(filtered_data, x='Year', y='ANNUAL RAINFALL (Millimeters)', title=f"Rainfall Trend for {selected_district} in {latest_year}")
st.plotly_chart(fig)

# Additional Interactive Chart for Water Balance
data_for_chart = filtered_data.copy()
data_for_chart['Water Balance'] = data_for_chart['ANNUAL RAINFALL (Millimeters)'] - data_for_chart[
    [col for col in evapotranspiration_data.columns if 'POTENTIAL' in col]].sum(axis=1)
fig_water_balance = px.line(data_for_chart, x='Year', y='Water Balance', title=f"Water Balance Trend for {selected_district} in {latest_year}")
st.plotly_chart(fig_water_balance)

# Instructions for Running the Dashboard
st.markdown("### How to Run the Dashboard:")
st.markdown("1. Save this script as `irrigation_alert_dashboard.py`.")
st.markdown("2. Run `streamlit run irrigation_alert_dashboard.py` in your terminal.")
st.markdown("3. Open the provided URL in your browser to explore the dashboard.")
