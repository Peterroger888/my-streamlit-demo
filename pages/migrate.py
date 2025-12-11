# migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page")

# ----------------------------
# Read MongoDB credentials from Streamlit secrets
# ----------------------------
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]  # should be "mydb"

mongo_uri = f"mongodb+srv://{user}:{password}@cluster0.mongodb.net/{db_name}?retryWrites=true&w=majority"

# ----------------------------
# Function to connect to MongoDB safely
# ----------------------------
@st.cache_resource  # caches the connection to avoid reconnecting on every rerun
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 sec timeout
        client.server_info()  # force connection check
        return client[db_name]
    except errors.ServerSelectionTimeoutError as e:
        st.error(f"Could not connect to MongoDB: {e}")
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

    # Use the correct collection
    collection_name = "records"

    if st.button("Load Data from 'records' Collection"):
        with st.spinner("Loading data..."):
            try:
                collection = db[collection_name]
                data = list(collection.find())
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.info("No data found in the collection 'records'.")
            except Exception as e:
                st.error(f"Error reading collection '{collection_name}': {e}")
