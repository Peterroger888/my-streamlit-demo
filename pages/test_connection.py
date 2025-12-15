<<<<<<< HEAD
# test_connection.py
import streamlit as st
from pymongo import MongoClient, errors

st.title("MongoDB Connection Test")

# Read credentials from Streamlit secrets
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]

# ----------------------------
# SRV URI (mongodb+srv://)
srv_uri = f"mongodb+srv://{user}:{password}@cluster0.6hjrs.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Standard full URI (mongodb://) - replace hosts with your cluster hosts
standard_uri = (
    f"mongodb://{user}:{password}@"
    f"cluster0-shard-00-00.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-01.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-02.6hjrs.mongodb.net:27017/"
    f"{db_name}?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin&retryWrites=true&w=majority"
)

# ----------------------------
# Function to test a connection
def test_connection(uri, label):
    st.write(f"Testing {label} URI...")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        st.write("Created MongoClient")
        client.server_info()  # force connection
        st.success(f"{label} connection successful!")
        db = client[db_name]
        collections = db.list_collection_names()
        st.write(f"Collections in {db_name}: {collections}")
    except errors.ServerSelectionTimeoutError as e:
        st.error(f"{label} Server selection timeout: {e}")
    except errors.OperationFailure as e:
        st.error(f"{label} Authentication failed: {e}")
    except Exception as e:
        st.error(f"{label} Unexpected error: {e}")

# ----------------------------
# Run tests
if st.button("Test SRV URI"):
    test_connection(srv_uri, "SRV")

if st.button("Test Standard URI"):
    test_connection(standard_uri, "Standard")
=======
# test_connection.py
import streamlit as st
from pymongo import MongoClient, errors

st.title("MongoDB Connection Test")

# Read credentials from Streamlit secrets
user = st.secrets["mongo"]["db_user"]
password = st.secrets["mongo"]["db_token"]
db_name = st.secrets["mongo"]["db_name"]

# ----------------------------
# SRV URI (mongodb+srv://)
srv_uri = f"mongodb+srv://{user}:{password}@cluster0.6hjrs.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Standard full URI (mongodb://) - replace hosts with your cluster hosts
standard_uri = (
    f"mongodb://{user}:{password}@"
    f"cluster0-shard-00-00.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-01.6hjrs.mongodb.net:27017,"
    f"cluster0-shard-00-02.6hjrs.mongodb.net:27017/"
    f"{db_name}?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin&retryWrites=true&w=majority"
)

# ----------------------------
# Function to test a connection
def test_connection(uri, label):
    st.write(f"Testing {label} URI...")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        st.write("Created MongoClient")
        client.server_info()  # force connection
        st.success(f"{label} connection successful!")
        db = client[db_name]
        collections = db.list_collection_names()
        st.write(f"Collections in {db_name}: {collections}")
    except errors.ServerSelectionTimeoutError as e:
        st.error(f"{label} Server selection timeout: {e}")
    except errors.OperationFailure as e:
        st.error(f"{label} Authentication failed: {e}")
    except Exception as e:
        st.error(f"{label} Unexpected error: {e}")

# ----------------------------
# Run tests
if st.button("Test SRV URI"):
    test_connection(srv_uri, "SRV")

if st.button("Test Standard URI"):
    test_connection(standard_uri, "Standard")
>>>>>>> 0c677943fd3e00590098223fa70c379a4e3bb755
