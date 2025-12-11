# pages/migrate.py
import streamlit as st
from pymongo import MongoClient, errors
import pandas as pd

st.title("MongoDB Migration Page")

# ----------------------------
# Read MongoDB credentials from Streamlit secrets
# ----------------------------
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]  # e.g., "mydb"

# ----------------------------
# Full standard URI for Atlas (replace hosts and replica set from Atlas Connect -> Python)
# ----------------------------
mongo_uri = (
    f"mongodb://{user}:{password}@"
    f"cluster0-shard-00-00.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-01.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-02.6hjrs.mongodb.net:27017/"
    f"{db_name}?ssl=true&replicaSet=atlas-abc123-shard-0&authSource=admin&retryWrites=true&w=majority"
)

# ----------------------------
# Connect to MongoDB
# ----------------------------
@st.cache_resource  # caches connection
def get_db():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5s timeout
        client.server_info()  # force connection
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
