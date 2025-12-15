import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page")

# Read MongoDB URI from secrets
mongo_uri = st.secrets["mongo"]["uri"]

# Connect to MongoDB
@st.cache_resource
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # force connection
        db_name = mongo_uri.split("/")[-1].split("?")[0]  # extract DB from URI
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

# Main app
if db:
    st.success(f"Connected to MongoDB database: {db.name}")

    collection_name = "records"  # your collection

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
