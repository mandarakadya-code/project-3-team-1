import os
import psycopg2

DB_NAME = os.getenv("DB_NAME", "Climate_Change_Analysis")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

ALLOWED_TABLE_NAMES = ['annual_emissions', 'per_capita_emissions']

def fetch_table_data(table_name):
    # Validate the table_name to prevent SQL injection
    if table_name not in ALLOWED_TABLE_NAMES:
        raise ValueError(f"Invalid table name: {table_name}")

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Safe to use f-string here because table_name has been validated
            query = f"SELECT * FROM {table_name};"
            cur.execute(query)
            records = cur.fetchall()
            return records









