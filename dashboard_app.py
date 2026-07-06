import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery

# Page Configuration Setup
st.set_page_config(page_title="Enterprise Data Warehouse Monitor", layout="wide")

st.title("🛍️ Enterprise BigQuery Analytics Monitor")
st.markdown("Real-time metrics computed via **dbt Core** and hosted on **Google BigQuery**.")

PROJECT_ID = "analytics-engineering-learning"

@st.cache_data(ttl=60)
def fetch_bigquery_analytics_data():
    """Establishes a secure connection to BigQuery using file-based or multi-fallback secrets detection."""
    try:
        # 1. Local Development Fallback
        if os.path.exists("gcp_creds.json"):
            credentials = service_account.Credentials.from_service_account_file("gcp_creds.json")
            
        # 2. Production Environment Omni-Detection Engine
        else:
            creds_dict = None
            
            # Scenario A: Pasted as a flat list at the root of the Secrets panel
            if "private_key" in st.secrets:
                creds_dict = dict(st.secrets)
            # Scenario B: Pasted under a [gcp_service_account] section block
            elif "gcp_service_account" in st.secrets:
                creds_dict = dict(st.secrets["gcp_service_account"])
            # Scenario C: Pasted as a single compressed string block
            elif "BIGQUERY_JSON_STRING" in st.secrets:
                creds_dict = json.loads(st.secrets["BIGQUERY_JSON_STRING"])
                
            if creds_dict is not None:
                # 🛡️ Automatically clean internal hidden newline sequence mismatches
                if "private_key" in creds_dict:
                    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
                credentials = service_account.Credentials.from_service_account_info(creds_dict)
            else:
                # Helpful debug visualization to see what keys actually exist inside your settings console
                found_keys = list(st.secrets.keys())
                raise FileNotFoundError(f"No credential blocks detected. Active configuration keys found: {found_keys}")
            
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        # Target your full 25,000 row production e-commerce mart table
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
        st.metric(label="Total Platform Orders Captured (Production)", value=f"{total_orders:,}")
        
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
                status_df, x='Status', y='Total Orders', color='Status',
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with col2:
        st.subheader("👥 User Payment Method Allocation")
        if 'payment_method' in df_metrics.columns:
            fig_pie = px.pie(
                df_metrics, names='payment_method', hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- Live Data Ledger ---
    st.subheader("📋 Core Warehouse Ledger View (`analytics.fct_orders`)")
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ BigQuery analytical ledger is currently unpopulated. Verify pipeline execution.")