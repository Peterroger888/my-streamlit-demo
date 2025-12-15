<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import psycopg2

# --------------------------------
# Page config
# --------------------------------
st.set_page_config(
    page_title="Stock Monitor",
    layout="wide"
)

st.title("📈 Stock Market Dashboard")

# --------------------------------
# Database access (PostgreSQL via URI)
# --------------------------------
@st.cache_data(ttl=300)
def get_stock_data():
    conn = psycopg2.connect(st.secrets["postgres"]["uri"])

    query = """
        SELECT *
        FROM stock_price
        WHERE code IS NOT NULL
        ORDER BY today_date
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# --------------------------------
# Plot generator
# --------------------------------
def generate_plot(df, title, y_column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["today_date"],
        y=df[y_column],
        mode="lines+markers",
        name=title
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)" if y_column == "market_price" else "Market Value ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.3f",
        hovermode="x unified",
        xaxis=dict(
            tickangle=90,
            tickfont=dict(size=9),
            tickformat="%d-%b"
        ),
        height=500
    )

    return fig


# --------------------------------
# Load data
# --------------------------------
df = get_stock_data()

# --------------------------------
# Sidebar filter
# --------------------------------
stock_names = ["All"] + sorted(df["name"].dropna().unique().tolist())
selected_stock = st.sidebar.selectbox("Select Stock", stock_names)

# --------------------------------
# Data logic (Flask routes replaced)
# --------------------------------
if selected_stock == "All":
    df_plot = (
        df.groupby("today_date", as_index=False)["market_value"]
        .sum()
    )
    fig = generate_plot(
        df_plot,
        "Total Market Value",
        "market_value"
    )
else:
    df_plot = df[df["name"] == selected_stock]
    fig = generate_plot(
        df_plot,
        f"Stock Price - {selected_stock}",
        "market_price"
    )

# --------------------------------
# Render chart
# --------------------------------
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# Optional: data preview
# --------------------------------
with st.expander("Show data table"):
    st.dataframe(df_plot)
=======
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import psycopg2

# --------------------------------
# Page config
# --------------------------------
st.set_page_config(
    page_title="Stock Monitor",
    layout="wide"
)

st.title("📈 Stock Market Dashboard")

# --------------------------------
# Database access (PostgreSQL via URI)
# --------------------------------
@st.cache_data(ttl=300)
def get_stock_data():
    conn = psycopg2.connect(st.secrets["postgres"]["uri"])

    query = """
        SELECT *
        FROM stock_price
        WHERE code IS NOT NULL
        ORDER BY today_date
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# --------------------------------
# Plot generator
# --------------------------------
def generate_plot(df, title, y_column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["today_date"],
        y=df[y_column],
        mode="lines+markers",
        name=title
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)" if y_column == "market_price" else "Market Value ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.3f",
        hovermode="x unified",
        xaxis=dict(
            tickangle=90,
            tickfont=dict(size=9),
            tickformat="%d-%b"
        ),
        height=500
    )

    return fig


# --------------------------------
# Load data
# --------------------------------
df = get_stock_data()

# --------------------------------
# Sidebar filter
# --------------------------------
stock_names = ["All"] + sorted(df["name"].dropna().unique().tolist())
selected_stock = st.sidebar.selectbox("Select Stock", stock_names)

# --------------------------------
# Data logic (Flask routes replaced)
# --------------------------------
if selected_stock == "All":
    df_plot = (
        df.groupby("today_date", as_index=False)["market_value"]
        .sum()
    )
    fig = generate_plot(
        df_plot,
        "Total Market Value",
        "market_value"
    )
else:
    df_plot = df[df["name"] == selected_stock]
    fig = generate_plot(
        df_plot,
        f"Stock Price - {selected_stock}",
        "market_price"
    )

# --------------------------------
# Render chart
# --------------------------------
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# Optional: data preview
# --------------------------------
with st.expander("Show data table"):
    st.dataframe(df_plot)
>>>>>>> 0c677943fd3e00590098223fa70c379a4e3bb755
