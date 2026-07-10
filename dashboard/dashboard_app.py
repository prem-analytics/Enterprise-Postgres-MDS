import streamlit as st

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Enterprise Modern Data Stack",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.title("📊 Enterprise MDS")

    st.markdown("---")

    st.subheader("Project")

    st.write("**Version**")
    st.success("v1.0")

    st.write("**Environment**")
    st.info("Development")

    st.markdown("---")

    st.subheader("Technology")

    st.write("🐍 Python")
    st.write("🐘 PostgreSQL")
    st.write("☁ Google BigQuery")
    st.write("🌳 dbt Core")
    st.write("⚙ Dagster")
    st.write("📈 Streamlit")

    st.markdown("---")

    st.caption("Modern Data Stack")

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("📊 Enterprise Modern Data Stack")

st.markdown(
"""
Enterprise-grade Analytics Engineering Platform built with
**Python**, **PostgreSQL**, **Google BigQuery**, **dbt Core**, **Dagster**, and **Streamlit**.
"""
)

st.divider()

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Dashboards",
        "5"
    )

with col2:
    st.metric(
        "Pipelines",
        "2"
    )

with col3:
    st.metric(
        "Warehouse",
        "Online"
    )

with col4:
    st.metric(
        "Environment",
        "Development"
    )

st.divider()

# ----------------------------------------------------
# PROJECT OVERVIEW
# ----------------------------------------------------

st.header("📌 Project Overview")

st.write(
"""
This project demonstrates a complete **Enterprise Modern Data Stack**
covering the entire analytics engineering lifecycle.

The platform includes:

- REST API ingestion
- PostgreSQL Operational Warehouse
- dbt Transformations
- Google BigQuery Analytics Warehouse
- Dagster Orchestration
- Interactive Streamlit Dashboards
"""
)

st.divider()

# ----------------------------------------------------
# SYSTEM HEALTH
# ----------------------------------------------------

st.header("🟢 System Health")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("PostgreSQL")

with c2:
    st.success("BigQuery")

with c3:
    st.success("dbt")

with c4:
    st.success("Dagster")

st.divider()

# ----------------------------------------------------
# ARCHITECTURE
# ----------------------------------------------------

st.header("🏗 Architecture")

st.code(
"""
REST API
    │
    ▼
PostgreSQL
    │
    ▼
dbt Core
    │
    ▼
Google BigQuery
    │
    ▼
Streamlit Dashboard
""",
language="text"
)

st.divider()

# ----------------------------------------------------
# FEATURES
# ----------------------------------------------------

st.header("🚀 Platform Features")

left, right = st.columns(2)

with left:

    st.markdown("""
### Data Engineering

- REST API Ingestion
- PostgreSQL
- SQL
- Python
- ETL Pipelines
- Data Validation
""")

with right:

    st.markdown("""
### Analytics Engineering

- dbt Core
- Google BigQuery
- Dagster
- Streamlit
- Plotly
- Interactive Dashboards
""")

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption(
"""
Enterprise Modern Data Stack

Version 1.0

Built with Python • PostgreSQL • BigQuery • dbt • Dagster • Streamlit
"""
)