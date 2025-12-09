import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="CSV Viewer", layout="wide")
st.title("CSV Data Display with External HTML, CSS & JS")

# Upload CSV or use default
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/data.csv")  # default CSV

# Convert DataFrame to HTML
table_html = df.to_html(index=False, classes="csv-table")

# Load external HTML template
with open("table.html", "r") as f:
    html_template = f.read()

# Replace placeholder table with actual table
html_content = html_template.replace('<table id="csvTable" class="csv-table"></table>', table_html)

# Include external CSS
st.markdown('<link rel="stylesheet" href="static/css/style.css">', unsafe_allow_html=True)

# Render HTML + JS
components.html(html_content, height=500, scrolling=True)
