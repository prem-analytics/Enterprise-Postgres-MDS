import os
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# 1. Page Configuration Setup
st.set_page_config(page_title="Postgres Data Warehouse Monitor", layout="wide")

st.title("🛍️ Enterprise Neon Postgres Analytics Monitor")
st.markdown("Real-time metrics computed via **dbt Core** and hosted on **Neon PostgreSQL**.")

@st.cache_data(ttl=60) # Caches data for 60 seconds to protect database compute limits
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
        
        # 🎯 TARGET THE NEWLY CREATED POSTGRES TABLE
        query = "SELECT * FROM analytics.fct_user_post_metrics;"
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
    kpi1, kpi2 = st.columns(2)
    
    with kpi1:
        total_users = df_metrics['user_id'].nunique() if 'user_id' in df_metrics.columns else 0
        st.metric(label="Total Active Users Monitored", value=f"{total_users:,}")
        
    with kpi2:
        total_records = len(df_metrics)
        st.metric(label="Total Aggregated Metric Records", value=f"{total_records:,}")

    st.markdown("---")
    
    # --- Dynamic Interactive Charts ---
    # Automatically finds numeric metrics inside your dbt model to display dynamically
    numeric_cols = df_metrics.select_dtypes(include=['number']).columns.tolist()
    # Exclude user_id from charts if it got typed as a number
    if 'user_id' in numeric_cols:
        numeric_cols.remove('user_id')
        
    if numeric_cols:
        st.subheader("🎯 Enterprise Metrics Performance Distribution")
        col_to_plot = numeric_cols[0] # Plots the primary computed dbt metric
        
        fig_bar = px.bar(
            df_metrics, 
            x='user_id' if 'user_id' in df_metrics.columns else df_metrics.index, 
            y=col_to_plot,
            title=f"Distribution of {col_to_plot.replace('_', ' ').title()} by User",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Additional performance visualization metrics will appear here as columns grow.")

    # --- Live Data Ledger ---
    st.subheader("📋 Core Warehouse Ledger View (`analytics.fct_user_post_metrics`)")
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Postgres analytical ledger is currently unpopulated. Run your pipeline to stream metrics.")