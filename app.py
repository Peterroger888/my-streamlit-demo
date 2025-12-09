import streamlit as st
import pandas as pd
from utils.helper import get_summary_stats

st.title("My Streamlit Demo App")

st.write("This is a simple app deployed from GitHub → Streamlit Community Cloud.")

# Load sample data
df = pd.read_csv("data/sample.csv")

st.subheader("📊 Sample Data")
st.dataframe(df)

# Summary statistics using helper module
st.subheader("📈 Summary Statistics")
stats = get_summary_stats(df)
st.json(stats)

# Upload a CSV
st.subheader("📤 Upload your own CSV")
uploaded = st.file_uploader("Choose CSV", type="csv")

if uploaded:
    user_df = pd.read_csv(uploaded)
    st.dataframe(user_df)
    st.write("Summary:")
    st.json(get_summary_stats(user_df))
