import os
import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery

# 1. Authenticate using your secure absolute key file path
CREDS_PATH = "D:/Enterprise-Postgres-MDS/gcp_creds.json"
credentials = service_account.Credentials.from_service_account_file(CREDS_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# 2. Configure target settings
PROJECT_ID = "analytics-engineering-learning"
STAGING_DATASET = "staging"

def generate_mock_data(num_customers=5000, num_orders=50000):
    print(f"🚀 Generating {num_customers} customers and {num_orders} historical orders...")
    
    # Generate Customers
    customer_ids = [str(uuid.uuid4())[:8] for _ in range(num_customers)]
    countries = ['US', 'CA', 'GB', 'DE', 'FR', 'JP', 'IN', 'AU']
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'first_name': [f"User_{i}" for i in range(num_customers)],
        'country': [random.choice(countries) for _ in range(num_customers)],
        'created_at': [datetime.now() - timedelta(days=random.randint(1, 365)) for _ in range(num_customers)]
    })
    
    # Generate Orders
    order_statuses = ['completed', 'completed', 'completed', 'returned', 'shipped', 'placed']
    payment_methods = ['credit_card', 'paypal', 'apple_pay', 'crypto']
    
    orders_df = pd.DataFrame({
        'order_id': [str(uuid.uuid4())[:12] for _ in range(num_orders)],
        'customer_id': [random.choice(customer_ids) for _ in range(num_orders)],
        'order_date': [datetime.now() - timedelta(days=random.randint(0, 180)) for _ in range(num_orders)],
        'status': [random.choice(order_statuses) for _ in range(num_orders)],
        'order_total': [round(random.uniform(10.50, 750.00), 2) for _ in range(num_orders)],
        'payment_method': [random.choice(payment_methods) for _ in range(num_orders)]
    })
    
    return customers_df, orders_df

def load_to_bigquery(df, table_name):
    target_table = f"{PROJECT_ID}.{STAGING_DATASET}.{table_name}"
    print(f"📦 Streaming data into BigQuery target: {target_table}...")
    
    # Configure an overwrite write disposition to keep portfolio refreshes clean
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    job = client.load_table_from_dataframe(df, target_table, job_config=job_config)
    job.result()  # Wait for the cloud upload confirmation completely
    print(f"✅ Successfully loaded {len(df)} rows into {table_name}!")

if __name__ == "__main__":
    # Generate high volume transactional objects
    customers_df, orders_df = generate_mock_data(num_customers=2500, num_orders=25000)
    
    # Execute structural warehouse shipments
    load_to_bigquery(customers_df, "raw_customers")
    load_to_bigquery(orders_df, "raw_orders")
    print("\n🌟 Ingestion Pipeline successfully completed!")