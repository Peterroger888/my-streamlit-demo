import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.title("CSV → MongoDB Migration Tool")

# Load CSV
df = pd.read_csv("data/data.csv")

# Connect to MongoDB
client = MongoClient(st.secrets["mongo_uri"])
db = client["mydb"]
collection = db["records"]

# Clear collection
collection.delete_many({})

# Convert DF to records
records = df.to_dict(orient="records")

# Insert records
if st.button("Run Migration Now"):
    if records:
        collection.insert_many(records)
        st.success(f"Inserted {len(records)} records into MongoDB!")
    else:
        st.error("CSV is empty — nothing migrated.")
