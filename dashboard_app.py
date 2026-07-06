import os
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
    """Connect to BigQuery and fetch analytics data."""

    try:

        # -----------------------------
        # LOCAL DEVELOPMENT
        # -----------------------------
        if os.path.exists("gcp_creds.json"):

            credentials = service_account.Credentials.from_service_account_file(
                "gcp_creds.json"
            )

        # -----------------------------
        # STREAMLIT CLOUD
        # -----------------------------
        else:

            st.write("Secret keys:", list(st.secrets["gcp_service_account"].keys()))

            pk = st.secrets["gcp_service_account"]["private_key"]

            st.write("Starts with:", repr(pk[:40]))
            st.write("Ends with:", repr(pk[-40:]))
            st.write("Length:", len(pk))

            credentials = service_account.Credentials.from_service_account_info(
                dict(st.secrets["gcp_service_account"])
            )

            client = bigquery.Client(
                credentials=credentials,
                project=PROJECT_ID
            )

            query = f"""
            SELECT *
            FROM `{PROJECT_ID}.analytics.fct_orders`
            """

        df = client.query(query).to_dataframe()

        return df

    except Exception as e:

        st.exception(e)

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