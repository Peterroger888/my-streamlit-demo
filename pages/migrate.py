# pages/migrate_postgres.py
import streamlit as st
import pandas as pd
import os
import psycopg2
from psycopg2 import sql, OperationalError

st.title("PostgreSQL Migration Page")

# ----------------------------
# Read PostgreSQL URI from secrets
# ----------------------------
postgres_uri = st.secrets["postgres"]["uri"]

# ----------------------------
# Connect to PostgreSQL
# ----------------------------
def get_conn():
    try:
        conn = psycopg2.connect(postgres_uri)
        return conn
    except OperationalError as e:
        st.error(f"Unable to connect to PostgreSQL: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

conn = get_conn()

# ----------------------------
# Create table if it doesn't exist
# ----------------------------
def create_table_if_not_exists(conn, table_name):
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

# ----------------------------
# Insert CSV rows into table
# ----------------------------
def insert_csv(conn, table_name, df):
    if df.empty:
        st.info("CSV is empty, nothing to insert.")
        return
    try:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute(
                    sql.SQL("INSERT INTO {} (name, age, score) VALUES (%s, %s, %s)")
                    .format(sql.Identifier(table_name)),
                    (row['name'], row['age'], row['score'])
                )
            conn.commit()
        st.success(f"Inserted {len(df)} records into '{table_name}'")
    except Exception as e:
        st.error(f"Error inserting data: {e}")

# ----------------------------
# Load table data into DataFrame
# ----------------------------
def load_table(conn, table_name):
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        return df
    except Exception as e:
        st.error(f"Error reading table '{table_name}': {e}")
        return pd.DataFrame()

# ----------------------------
# Main App
# ----------------------------
if conn is not None:
    table_name = "records"
    st.write(f"Connected to PostgreSQL database: '{conn.get_dsn_parameters()['dbname']}', table: '{table_name}'")

    create_table_if_not_exists(conn, table_name)

    # --- Step 1: Load CSV ---
    csv_path = os.path.join("data", "data.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.write("CSV Preview:", df)

        # --- Step 2: Upload to PostgreSQL ---
        if st.button("Upload CSV to PostgreSQL"):
            insert_csv(conn, table_name, df)
    else:
        st.warning(f"CSV file not found at {csv_path}")

    # --- Step 3: Display table ---
    if st.button(f"Load Data from '{table_name}'"):
        df_table = load_table(conn, table_name)
        if not df_table.empty:
            st.dataframe(df_table)
        else:
            st.info(f"No data found in '{table_name}'.")
