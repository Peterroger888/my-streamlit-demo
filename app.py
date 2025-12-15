import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import psycopg2
import os

# -------------------------------
# 1️⃣ Database configuration
# -------------------------------
# Make sure you set the environment variable POSTGRES_URI in Streamlit secrets
DATABASE_URL = st.secrets["postgres"]["uri"]

# -------------------------------
# 2️⃣ Function to fetch stock data
# -------------------------------
@st.cache_data(ttl=600)
def get_stock_data():
    """Fetch latest stock data from PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        query = "SELECT * FROM stock_price"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# -------------------------------
# 3️⃣ Function to generate Plotly chart
# -------------------------------
fig.update_layout(
    title=f"Stock Price - {name}",
    xaxis_title="Date",
    yaxis_title="Price ($)" if y_column == 'market_price' else "Market Value ($)",
    yaxis_tickprefix='$',
    yaxis_tickformat=',.3f',
    hovermode='x unified',
    height=600,
    margin=dict(l=40, r=40, t=60, b=120),  # extra bottom space for 90° labels
    xaxis=dict(
        dtick=604800000,      # weekly ticks
        tickangle=90,         # your preference
        tickfont=dict(size=8),
        tickformat="%d-%b",
        automargin=True       # IMPORTANT for vertical labels
    )
)

# -------------------------------
# 4️⃣ Fetch data
# -------------------------------
df = get_stock_data()

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# -------------------------------
# 5️⃣ Sidebar: Select Stock
# -------------------------------
stock_names = ['All'] + sorted(df['name'].dropna().astype(str).unique())

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stock_names,
    key="unique_stock_selectbox"
)

# -------------------------------
# 6️⃣ Filter data for chart
# -------------------------------
if selected_stock == "All":
    df_filtered = df.groupby('today_date', as_index=False)['market_value'].sum()
    chart_fig = generate_plot(df_filtered, 'Total Market Value', y_column='market_value')
else:
    df_filtered = df[df['name'] == selected_stock]
    chart_fig = generate_plot(df_filtered, selected_stock, y_column='market_price')

# -------------------------------
# 7️⃣ Render chart
# -------------------------------
st.plotly_chart(chart_fig, use_container_width=True)
