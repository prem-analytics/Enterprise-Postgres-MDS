import os
import json
import base64
import pathlib
import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery

# 1. Page Configuration Setup
st.set_page_config(page_title="BigQuery Data Warehouse Monitor", layout="wide")

st.title("🛍️ Enterprise BigQuery Analytics Monitor")
st.markdown("Real-time metrics computed via **dbt Core** and hosted on **Google BigQuery**.")

# Infrastructure Routing Constants
PROJECT_ID = "analytics-engineering-learning"

@st.cache_data(ttl=60) # Caches results for 60 seconds to protect your BigQuery query bytes limits
def fetch_bigquery_analytics_data():
    """Establishes a secure connection using either a cloud base64 string or local service keys."""
    try:
        # 🌟 FOOLPROOF BASE64 CLOUD CHECKER
        if "gcp_creds_b64" in st.secrets:
            b64_data = st.secrets["gcp_creds_b64"]
            # Decode the unbroken text string straight back into clean raw JSON
            json_creds = base64.b64decode(b64_data).decode("utf-8")
            creds_dict = json.loads(json_creds)
            credentials = service_account.Credentials.from_service_account_info(creds_dict)
            
        elif "gcp_service_account" in st.secrets or "gcp_creds_json" in st.secrets:
            # Traditional fallback parsing layers
            creds_info = st.secrets.get("gcp_service_account") or st.secrets.get("gcp_creds_json")
            if isinstance(creds_info, str):
                creds_dict = json.loads(creds_info)
            else:
                creds_dict = dict(creds_info)
            if "private_key" in creds_dict and isinstance(creds_dict["private_key"], str):
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            credentials = service_account.Credentials.from_service_account_info(creds_dict)
            
        else:
            # Fallback to local path for your offline development environment
            CREDS_PATH = "D:/Enterprise-Postgres-MDS/gcp_creds.json"
            credentials = service_account.Credentials.from_service_account_file(CREDS_PATH)
            
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        # Target your pristine dbt final fact table mart
        query = f"SELECT * FROM `{PROJECT_ID}.analytics.fct_orders`;"
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        st.error(f"❌ BigQuery Warehouse Linkage Error: {e}")
        return pd.DataFrame()

# Execute data extraction pipeline
df_metrics = fetch_bigquery_analytics_data()

if not df_metrics.empty:
    # --- KPI Blocks ---
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        total_customers = df_metrics['customer_id'].nunique() if 'customer_id' in df_metrics.columns else 0
        st.metric(label="Total Active Customers Monitored", value=f"{total_customers:,}")
        
    with kpi2:
        total_orders = len(df_metrics)
        st.metric(label="Total Platform Orders Captured", value=f"{total_orders:,}")
        
    with kpi3:
        total_revenue = df_metrics['order_total_usd'].sum() if 'order_total_usd' in df_metrics.columns else 0.0
        st.metric(label="Gross Generated Warehouse Revenue", value=f"${total_revenue:,.2f}")

    st.markdown("---")
    
    # --- Interactive Charts ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Order Fulfilment Status Volume")
        if 'order_status' in df_metrics.columns:
            status_df = df_metrics['order_status'].value_counts().reset_index()
            status_df.columns = ['Status', 'Total Orders']
            fig_bar = px.bar(
                status_df, 
                x='Status', 
                y='Total Orders', 
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Status tracking data unavailable.")
            
    with col2:
        st.subheader("👥 User Payment Method Allocation")
        if 'payment_method' in df_metrics.columns:
            fig_pie = px.pie(
                df_metrics, 
                names='payment_method', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- Live Data Ledger ---
    st.subheader("📋 Core Warehouse Ledger View (`analytics.fct_orders`)")
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ BigQuery analytical ledger is currently unpopulated. Run your Dagster pipeline to stream metrics.")