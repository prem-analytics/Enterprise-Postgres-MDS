import streamlit as st
import pandas as pd
import plotly.express as px

from config.config import (
    PAGE_TITLE,
    PAGE_LAYOUT,
    CACHE_TIME,
)

from services.bigquery_service import (
    fetch_bigquery_analytics_data,
    get_tables,
    get_dataset_statistics,
    get_row_count,
    get_columns,
    preview_table,
    execute_query,
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="☁",
    layout=PAGE_LAYOUT,
)

st.title("☁ Google BigQuery Analytics Warehouse")

st.markdown("""
Enterprise Analytics Warehouse powered by **Google BigQuery**.
""")

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data(ttl=CACHE_TIME)
def load_data():
    return fetch_bigquery_analytics_data()

df_metrics = load_data()

tables_df = get_tables()
dataset_stats = get_dataset_statistics()

# ==========================================================
# WAREHOUSE OVERVIEW
# ==========================================================

st.header("🏢 Warehouse Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Project",
        "analytics-engineering-learning"
    )

with k2:
    st.metric(
        "Dataset",
        "analytics"
    )

with k3:
    st.metric(
        "Tables",
        int(dataset_stats.iloc[0]["tables"])
    )

with k4:
    st.metric(
        "Warehouse Rows",
        f"{len(df_metrics):,}"
    )

st.divider()

# ==========================================================
# ANALYTICS KPIs
# ==========================================================

st.header("📊 Business KPIs")

c1, c2, c3 = st.columns(3)

with c1:

    total_customers = (
        df_metrics["customer_id"].nunique()
        if "customer_id" in df_metrics.columns
        else 0
    )

    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with c2:

    st.metric(
        "Orders",
        f"{len(df_metrics):,}"
    )

with c3:

    if "order_total_usd" in df_metrics.columns:

        revenue = (
            pd.to_numeric(
                df_metrics["order_total_usd"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    else:

        revenue = 0

    st.metric(
        "Revenue",
        f"${revenue:,.2f}"
    )

st.divider()

# ==========================================================
# DATASET EXPLORER
# ==========================================================

st.header("📂 Dataset Explorer")

selected_table = st.selectbox(
    "Select Table",
    tables_df["table_name"]
)

rows = get_row_count(selected_table)

st.metric(
    "Rows in Selected Table",
    f"{rows:,}"
)

st.divider()

# ==========================================================
# COLUMN METADATA
# ==========================================================

st.header("📋 Column Metadata")

columns = get_columns(selected_table)

st.dataframe(
    columns,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# TABLE PREVIEW
# ==========================================================

st.header("👀 Table Preview")

preview = preview_table(
    selected_table,
    20
)

st.dataframe(
    preview,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# ANALYTICS CHARTS
# ==========================================================

st.header("📈 Business Analytics")

left, right = st.columns(2)

with left:

    if "order_status" in df_metrics.columns:

        status_df = (
            df_metrics["order_status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Orders"
        ]

        fig = px.bar(
            status_df,
            x="Status",
            y="Orders",
            color="Status",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

with right:

    if "payment_method" in df_metrics.columns:

        fig = px.pie(
            df_metrics,
            names="payment_method",
            hole=0.4,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

st.divider()

# ==========================================================
# SQL QUERY RUNNER
# ==========================================================

st.header("📝 SQL Query Runner")

default_sql = f"""
SELECT *
FROM `analytics-engineering-learning.analytics.{selected_table}`
LIMIT 20;
"""

query = st.text_area(
    "SQL Query",
    value=default_sql,
    height=180,
)

if st.button("▶ Run Query"):

    try:

        result = execute_query(query)

        st.success("Query executed successfully.")

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
        )

    except Exception as e:

        st.error(e)

st.divider()

# ==========================================================
# FACT TABLE DATA
# ==========================================================

st.header("📑 Fact Table Data")

st.dataframe(
    df_metrics,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.success("✅ BigQuery Warehouse Dashboard Loaded Successfully")