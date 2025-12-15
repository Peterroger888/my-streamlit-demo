import streamlit as st
import pandas as pd

# Example: your df from PostgreSQL
# df = get_stock_data()

# -------------------------------
# Sidebar: Select Stock
# -------------------------------

# Ensure only unique, non-empty names appear in the sidebar
stock_names = ['All'] + sorted(df['name'].dropna().astype(str).unique())

# Add a unique key to prevent duplicate element IDs
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stock_names,
    key="unique_stock_selectbox"
)

# -------------------------------
# Filter data based on selection
# -------------------------------
if selected_stock == "All":
    df_filtered = df.copy()
else:
    df_filtered = df[df['name'] == selected_stock]

# -------------------------------
# Generate chart (Plotly example)
# -------------------------------
import plotly.graph_objs as go

fig = go.Figure()
for stock_name, stock_data in df_filtered.groupby('name'):
    fig.add_trace(go.Scatter(
        x=stock_data['today_date'],
        y=stock_data['market_price'],
        mode='lines+markers',
        name=stock_name
    ))

fig.update_layout(
    title=f"Stock Prices - {selected_stock}",
    xaxis_title="Date",
    yaxis_title="Price (SGD)",
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
