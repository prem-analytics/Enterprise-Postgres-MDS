import psycopg2
import requests
import pandas as pd
import random
import os
from dotenv import load_dotenv

# Load variables from the hidden .env file
load_dotenv()

def ingest_api_to_postgres():
    print("[INFO] Initializing enterprise network connection to REST API endpoint...")
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        print("[INFO] API extraction pipeline stream successfully buffered.")
    except Exception as e:
        print(f"[ERROR] API Network Stage Aborted: {e}")
        return

    # Structure data into tabular frames (Safely processed right after assignment)
    full_df = pd.DataFrame(raw_data)

    # Simulating live incremental ingestion layer by processing random sample batches
    sample_size = random.randint(40, 80)
    df = full_df.sample(n=sample_size).reset_index(drop=True)
    print(f"[INFO] Simulating live incremental ingestion layer: Processing {sample_size} records...")

    print("[INFO] Establishing secure connection pool to PostgreSQL Warehouse...")
    try:
        # Secure credential extraction using environment variables
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
    except Exception as e:
        print(f"[ERROR] Database Connection Failed: {e}")
        return

    print("[INFO] Constructing production schemas and raw landing matrices...")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staging.stg_raw_posts (
            id INT PRIMARY KEY,
            user_id INT,
            title TEXT,
            body TEXT
        );
    """)
    
    # Wipe the old rows rapidly without breaking downstream dbt view mappings
    cursor.execute("TRUNCATE TABLE staging.stg_raw_posts;")

    print("[INFO] Initiating high-speed transactional row ingestion...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO staging.stg_raw_posts (id, user_id, title, body)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                title = EXCLUDED.title,
                body = EXCLUDED.body;
        """, (int(row['id']), int(row['userId']), str(row['title']), str(row['body'])))

    # Commit changes safely to log transactions
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM staging.stg_raw_posts;")
    rows_landed = cursor.fetchone()[0]
    print(f"[SUCCESS] Ingestion Phase Complete! Landed {rows_landed} master rows into postgres table 'staging.stg_raw_posts'.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    ingest_api_to_postgres()