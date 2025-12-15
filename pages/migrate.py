<<<<<<< HEAD
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
=======
# pages/migrate_postgres.py
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

st.title("PostgreSQL Migration Page")

# ----------------------------
# Read PostgreSQL URI from secrets
# ----------------------------
postgres_uri = st.secrets["postgres"]["uri"]

# ----------------------------
# Connect to PostgreSQL (cached)
# ----------------------------
@st.cache_resource
def get_conn():
    try:
        conn = psycopg2.connect(postgres_uri)
        return conn
    except Exception as e:
        st.error(f"Unable to connect to PostgreSQL: {e}")
        return None

conn = get_conn()

if conn is not None:
    table_name = "records"
    db_name = conn.get_dsn_parameters()['dbname']
    st.write(f"Connected to PostgreSQL database: '{db_name}', table: '{table_name}'")

    # ----------------------------
    # Create table if not exists
    # ----------------------------
    def create_table_if_not_exists():
        try:
            with conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {} (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        age INT,
                        score INT
                    )
                """).format(sql.Identifier(table_name)))
                conn.commit()
        except Exception as e:
            st.error(f"Error creating table '{table_name}': {e}")

    create_table_if_not_exists()

    # ----------------------------
    # CSV upload via file_uploader
    # ----------------------------
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("CSV Preview:", df)

        if st.button("Upload CSV to PostgreSQL"):
            try:
                with conn.cursor() as cur:
                    # Batch insert using executemany
                    cur.executemany(
                        sql.SQL("INSERT INTO {} (name, age, score) VALUES (%s, %s, %s)")
                        .format(sql.Identifier(table_name)),
                        df[['name', 'age', 'score']].values.tolist()
                    )
                    conn.commit()
                st.success(f"Inserted {len(df)} records into '{table_name}'")
            except Exception as e:
                st.error(f"Error inserting data: {e}")

    # ----------------------------
    # Display table data
    # ----------------------------
    if st.button(f"Load Data from '{table_name}'"):
        try:
            df_table = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            if not df_table.empty:
                st.dataframe(df_table)
            else:
                st.info(f"No data found in '{table_name}'.")
        except Exception as e:
            st.error(f"Error reading table '{table_name}': {e}")
>>>>>>> 0c677943fd3e00590098223fa70c379a4e3bb755
