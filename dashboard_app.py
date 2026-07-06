import os
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# 1. Page Configuration Setup
st.set_page_config(page_title="Postgres Data Warehouse Monitor", layout="wide")

st.title("🛍️ Enterprise Neon Postgres Analytics Monitor")
st.markdown("Real-time metrics computed via **dbt Core** and hosted on **Neon PostgreSQL**.")

@st.cache_data(ttl=60) # Caches data for 60 seconds to protect database compute hours limits
def fetch_postgres_analytics_data():
    """Establishes a secure connection to the Neon Postgres database warehouse."""
    try:
        # Check if running on Streamlit Cloud secure secrets keyring
        if "DATABASE_URL" in st.secrets:
            db_url = st.secrets["DATABASE_URL"]
        else:
            # Fallback to local connection string for offline development environment
            db_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/neondb")
            
        # Initialize connection engine
        conn = psycopg2.connect(db_url)
        query = "SELECT * FROM analytics.fct_orders;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Postgres Warehouse Linkage Error: {e}")
        return pd.DataFrame()

# Execute data extraction pipeline
df_metrics = fetch_postgres_analytics_data()

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
    st.warning("⚠️ Postgres analytical ledger is currently unpopulated. Run your Dagster pipeline to stream metrics.")