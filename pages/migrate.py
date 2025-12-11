# pages/migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page")

# ----------------------------
# Read MongoDB URI from secrets
# ----------------------------
mongo_uri = st.secrets["mongo"]["uri"]

# ----------------------------
# Debug info
# ----------------------------
st.write("Attempting to connect to MongoDB Atlas...")
st.write("Mongo URI (hidden for security):", mongo_uri[:30] + "...")


# ----------------------------
# Connect to MongoDB
# ----------------------------
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        st.write("MongoClient created, checking server info...")
        client.server_info()  # force connection to test
        st.success("MongoDB connection successful!")
        # Extract DB name from URI
        db_name = mongo_uri.split("/")[-1].split("?")[0] or "mydb"
        st.write(f"Using database: {db_name}")
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

# ----------------------------
# Get database
# ----------------------------
db = get_db()

# ----------------------------
# Main app
# ----------------------------
if db is not None:  # <-- Fix for NotImplementedError
    collection_name = "records"  # Change to your collection
    st.write(f"Ready to load data from collection: '{collection_name}'")

    if st.button(f"Load Data from '{collection_name}'"):
        with st.spinner("Loading data..."):
            try:
                collection = db[collection_name]
                data = list(collection.find())
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.info(f"No data found in '{collection_name}'.")
            except Exception as e:
                st.error(f"Error reading collection '{collection_name}': {e}")
