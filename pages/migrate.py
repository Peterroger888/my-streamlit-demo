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
db_name = st.secrets["mongo"]["db_name"]

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

db = get_db()

# ----------------------------
# Main app
# ----------------------------
if db:
    st.success("Connected to MongoDB!")

    # Fetch list of collections for user to choose
    try:
        collections = db.list_collection_names()
        if collections:
            collection_name = st.selectbox("Select a collection", collections)

            if st.button("Load Data"):
                with st.spinner("Loading data..."):
                    try:
                        data = list(db[collection_name].find())
                        if data:
                            df = pd.DataFrame(data)
                            st.dataframe(df)
                        else:
                            st.info("No data found in this collection.")
                    except Exception as e:
                        st.error(f"Error reading collection: {e}")
        else:
            st.info("No collections found in the database.")
    except Exception as e:
        st.error(f"Error fetching collections: {e}")
