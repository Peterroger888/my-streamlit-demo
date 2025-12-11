# migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page (Streamlit Cloud Ready)")

# ----------------------------
# Read MongoDB credentials from Streamlit secrets
# ----------------------------
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]  # should be "mydb"

# ----------------------------
# MongoDB URI
# Use SRV if you want: mongodb+srv://
# If SRV hangs on Streamlit Cloud, replace with full standard URI
# ----------------------------
mongo_uri = f"mongodb+srv://{user}:{password}@cluster0.6hjrs.mongodb.net/{db_name}?retryWrites=true&w=majority"

# ----------------------------
# Connect to MongoDB
# ----------------------------
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5s timeout
        client.server_info()  # forces connection check
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
if db:
    st.success(f"Connected to MongoDB database: {db_name}")

    # Collection to load
    collection_name = "records"

    if st.button(f"Load Data from '{collection_name}' Collection"):
        with st.spinner("Loading data..."):
            try:
                collection = db[collection_name]
                data = list(collection.find())
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.info(f"No data found in the collection '{collection_name}'.")
            except Exception as e:
                st.error(f"Error reading collection '{collection_name}': {e}")
