import streamlit as st
import pathlib

st.title("Streamlit + External HTML Example")

# Path to external HTML
html_path = pathlib.Path("static/external_page.html")

# Read the HTML
if html_path.exists():
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Display inside Streamlit
    st.components.v1.html(html_content, height=600, scrolling=True)
else:
    st.error("HTML file not found at: static/external_page.html")
