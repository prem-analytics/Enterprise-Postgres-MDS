import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os
from dotenv import load_dotenv

# 🌟 ENTERPRISE FIX: Read the configuration variables from your secure hidden .env file
load_dotenv()

# Setup page presentation
st.set_page_config(page_title="Data Warehouse Monitor", layout="wide")

st.title("📊 Enterprise Database Analytics Monitor")
st.markdown("Real-time metrics computed via **dbt Core** and hosted on **PostgreSQL 18**.")

def fetch_analytics_data():
    try:
        # Check if running on Streamlit Cloud using the unified connection string
        if "CONNECTION_STRING" in st.secrets:
            conn = psycopg2.connect(st.secrets["CONNECTION_STRING"])
        else:
            # Fallback to local .env processing keys for your local VS Code terminal
            conn = psycopg2.connect(
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                sslmode="require"
            )
        
        query = "SELECT * FROM analytics.fct_user_post_metrics ORDER BY user_id;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Warehouse Linkage Error: {e}")
        return pd.DataFrame()

df_metrics = fetch_analytics_data()

if not df_metrics.empty:
    # --- KPI Blocks ---
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Total Active Users Monitored", value=int(df_metrics['user_id'].nunique()))
    with kpi2:
        st.metric(label="Total Platform Posts Captured", value=int(df_metrics['total_posts_created'].sum()))
    with kpi3:
        st.metric(label="Average Character Length Across Users", value=f"{df_metrics['average_post_length_characters'].mean():.1f} ch")

    st.markdown("---")
    
    # --- Interactive Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Content Creation Volume")
        fig_bar = px.bar(df_metrics, x='user_id', y='total_posts_created', color='total_posts_created')
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.subheader("👥 User Engagement Allocation")
        fig_pie = px.pie(df_metrics, names='user_engagement_tier', values='total_posts_created')
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Live Data Ledger ---
    st.subheader("📋 Core Warehouse Ledger View (`analytics.fct_user_post_metrics`)")
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Warehouse ledger is currently unpopulated.")