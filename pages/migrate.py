# migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page (Debug Mode)")

# ----------------------------
# Read MongoDB credentials from Streamlit secrets
# ----------------------------
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]  # should be "mydb"

# ----------------------------
# Standard URI (non-SRV) recommended for cloud deployment
# Replace the hosts with your cluster's hosts from Atlas
# Example:
# cluster0-shard-00-00.abcde.mongodb.net:27017,cluster0-shard-00-01.abcde.mongodb.net:27017,...
# ----------------------------
mongo_uri = (
    f"mongodb://{user}:{password}@cluster0-shard-00-00.abcde.mongodb.net:27017,"
    f"cluster0-shard-00-01.abcde.mongodb.net:27017,"
    f"cluster0-shard-00-02.abcde.mongodb.net:27017/"
    f"{db_name}?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin&retryWrites=true&w=majority"
)

# ----------------------------
# Function to connect to MongoDB safely
# ----------------------------
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 sec timeout
        client.server_info()  # force connection check
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

    # Select collection (you said 'records')
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
