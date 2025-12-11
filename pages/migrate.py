# pages/migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd
import os

st.title("MongoDB Migration Page")

# ----------------------------
# Read MongoDB URI from secrets
# ----------------------------
mongo_uri = st.secrets["mongo"]["uri"]

# ----------------------------
# Connect to MongoDB
# ----------------------------
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # force connection
        db_name = mongo_uri.split("/")[-1].split("?")[0] or "mydb"
        return client[db_name]
    except errors.ServerSelectionTimeoutError as e:
        st.error(f"Server selection timeout: {e}")
        return None
    except errors.OperationFailure as e:
        st.error(f"Authentication failed: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

db = get_db()

# ----------------------------
# Main app
# ----------------------------
if db is not None:
    collection_name = "records"
    st.write(f"Connected to DB '{db.name}', collection '{collection_name}'")

    # --- Step 1: Load CSV ---
    csv_path = os.path.join("data", "data.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.write("CSV Preview:", df)
        
        # --- Step 2: Upload to MongoDB ---
        if st.button("Upload CSV to MongoDB"):
