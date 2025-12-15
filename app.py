import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import json

# -------------------------------
# 1️⃣ Fetch stock data
# -------------------------------
df = get_stock_data()  # Make sure this function is defined and returns a DataFrame

# -------------------------------
# 2️⃣ Prepare unique stock names for sidebar
# -------------------------------
stock_names = ['All'] + sorted(df['name'].dropna().astype(str).unique())

# Use a unique key to avoid StreamlitDuplicateElementId
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stock_names,
    key="unique_stock_selectbox"
)

# -------------------------------
# 3️⃣ Filter data based on selection
# -------------------------------
if selected_stock == "All":
    # Aggregate all stocks by date for "All"
    df_filtered = df.groupby('today_date', as_index=False)['market_value'].sum()
    chart_json = generate_plot(df_filtered, 'Total Market Value', y_column='market_value')
else:
    # Filter for the selected stock
    df_filtered = df[df['name'] == selected_stock]
    chart_json = generate_plot(df_filtered, selected_stock, y_column='market_price')

# -------------------------------
# 4️⃣ Render chart
# -------------------------------
st.plotly_chart(json.loads(chart_json), use_container_width=True)
