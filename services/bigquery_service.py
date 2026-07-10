import os
import pandas as pd
import streamlit as st

from google.oauth2 import service_account
from google.cloud import bigquery
from config.config import (
    PROJECT_ID,
    BIGQUERY_DATASET,
    FACT_TABLE,
)

# =======================================================
# BigQuery Connection
# =======================================================

def get_client():

    if os.path.exists("gcp_creds.json"):

        credentials = service_account.Credentials.from_service_account_file(
            "gcp_creds.json"
        )

    else:

        info = dict(st.secrets["gcp_service_account"])

        info["private_key"] = info["private_key"].replace("\\n", "\n")

        credentials = service_account.Credentials.from_service_account_info(
            info
        )

    return bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID,
    )


# =======================================================
# Execute Query
# =======================================================

def execute_query(query):

    client = get_client()

    df = client.query(query).to_dataframe()

    # Force all object columns to string
    for col in df.columns:

        if df[col].dtype == "object":
            df[col] = df[col].astype(str)

    return df


# =======================================================
# Main Analytics Table
# =======================================================

def fetch_bigquery_analytics_data():

    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{FACT_TABLE}`
    """

    return execute_query(query)


# =======================================================
# List Tables
# =======================================================

def get_tables():

    query = f"""
    SELECT
        table_name
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.INFORMATION_SCHEMA.TABLES`
    ORDER BY table_name
    """

    return execute_query(query)


# =======================================================
# Preview Table
# =======================================================

def preview_table(table, limit=20):

    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{table}`
    LIMIT {limit}
    """

    return execute_query(query)


# =======================================================
# Row Count
# =======================================================

def get_row_count(table):

    query = f"""
    SELECT COUNT(*) AS total_rows
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{table}`
    """

    return int(execute_query(query)["total_rows"][0])


# =======================================================
# Column Metadata
# =======================================================

def get_columns(table):

    query = f"""
    SELECT

        column_name,
        data_type,
        is_nullable

    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.INFORMATION_SCHEMA.COLUMNS`

    WHERE table_name='{table}'

    ORDER BY ordinal_position
    """

    return execute_query(query)


# =======================================================
# Dataset Statistics
# =======================================================

def get_dataset_statistics():

    query = f"""
    SELECT
        COUNT(*) AS tables
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.INFORMATION_SCHEMA.TABLES`
    """

    return execute_query(query)

# ======================================================
# Data Quality Functions
# ======================================================

def get_null_statistics(table):

    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{table}`
    LIMIT 1000
    """

    df = execute_query(query)

    stats = []

    for col in df.columns:

        nulls = df[col].isna().sum()

        stats.append({
            "Column": col,
            "Null Count": nulls,
            "Null %": round(
                nulls / len(df) * 100,
                2
            )
        })

    return pd.DataFrame(stats)


def get_duplicate_rows(table):

    df = preview_table(
        table,
        limit=5000
    )

    duplicates = df.duplicated().sum()

    return duplicates


def get_quality_score(table):

    df = preview_table(
        table,
        limit=5000
    )

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isna().sum().sum()

    score = (
        (total_cells - missing)
        / total_cells
    ) * 100

    return round(score, 2)


def get_distinct_values(table):

    df = preview_table(
        table,
        limit=5000
    )

    output = []

    for col in df.columns:

        output.append({
            "Column": col,
            "Distinct Values": df[col].nunique()
        })

    return pd.DataFrame(output)


def get_numeric_summary(table):

    df = preview_table(
        table,
        limit=5000
    )

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return pd.DataFrame()

    return numeric.describe()
# ==========================================================
# Custom SQL
# ==========================================================

def run_sql(query):

    return execute_query(query)

