import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from dagster import multi_asset, AssetOut

CREDS_PATH = "D:/Enterprise-Postgres-MDS/gcp_creds.json"
PROJECT_ID = "analytics-engineering-learning"
STAGING_DATASET = "staging"

@multi_asset(
    outs={
        "raw_customers": AssetOut(key_prefix="bq_staging"),
        "raw_orders": AssetOut(key_prefix="bq_staging"),
    },
    compute_kind="python"
)
def bq_raw_data_ingestion():
    """Generates high-volume enterprise e-commerce datasets and streams them to BigQuery."""
    num_customers = 2500
    num_orders = 25000
    
    # 1. Generate Customers
    customer_ids = [str(uuid.uuid4())[:8] for _ in range(num_customers)]
    countries = ['US', 'CA', 'GB', 'DE', 'FR', 'JP', 'IN', 'AU']
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'first_name': [f"User_{i}" for i in range(num_customers)],
        'country': [random.choice(countries) for _ in range(num_customers)],
        'created_at': [datetime.now() - timedelta(days=random.randint(1, 365)) for _ in range(num_customers)]
    })
    
    # 2. Generate Orders
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
    
    # 3. Stream Outbound Loads Directly to Google Cloud
    credentials = service_account.Credentials.from_service_account_file(CREDS_PATH)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    
    for df, table_name in [(customers_df, "raw_customers"), (orders_df, "raw_orders")]:
        target_table = f"{PROJECT_ID}.{STAGING_DATASET}.{table_name}"
        job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
        job = client.load_table_from_dataframe(df, target_table, job_config=job_config)
        job.result()
        
    return None, None