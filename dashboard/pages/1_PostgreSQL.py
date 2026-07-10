import os
import sys

# ============================================================
# Add project root to Python path
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from services.postgres_service import (
    get_version,
    get_database_size,
    get_active_connections,
    get_schema_count,
    get_database_statistics,
    get_tables,
    get_table_count,
    preview_table,
    get_columns,
    execute_query,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PostgreSQL Dashboard",
    page_icon="🐘",
    layout="wide",
)

st.title("🐘 PostgreSQL Dashboard")

st.markdown("""
Live monitoring dashboard for the PostgreSQL Operational Data Warehouse.
""")

st.divider()

# ============================================================
# LOAD DATABASE INFORMATION
# ============================================================

try:

    version = get_version()
    db_size = get_database_size()
    stats = get_database_statistics()
    connections = get_active_connections()
    schemas = get_schema_count()

except Exception as e:

    st.error(e)
    st.stop()

postgres_version = version.iloc[0]["version"].split(",")[0]
database_size = db_size.iloc[0]["database_size"]

tables_count = int(stats.iloc[0]["tables"])
views_count = int(stats.iloc[0]["views"])
indexes_count = int(stats.iloc[0]["indexes"])

active_connections = int(
    connections.iloc[0]["active_connections"]
)

schema_count = int(
    schemas.iloc[0]["schemas"]
)

# ============================================================
# KPI CARDS
# ============================================================

st.header("Database Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "PostgreSQL Version",
        postgres_version
    )

with k2:
    st.metric(
        "Database Size",
        database_size
    )

with k3:
    st.metric(
        "Schemas",
        schema_count
    )

with k4:
    st.metric(
        "Active Connections",
        active_connections
    )

k5, k6, k7 = st.columns(3)

with k5:
    st.metric(
        "Tables",
        tables_count
    )

with k6:
    st.metric(
        "Views",
        views_count
    )

with k7:
    st.metric(
        "Indexes",
        indexes_count
    )

st.divider()

# ============================================================
# TABLE EXPLORER
# ============================================================

st.header("📂 Table Explorer")

tables_df = get_tables()

tables_df["Display"] = (
    tables_df["table_schema"]
    + "."
    + tables_df["table_name"]
)

selected = st.selectbox(
    "Select Table",
    tables_df["Display"]
)

schema, table = selected.split(".")

st.info(
    f"Selected Table : {schema}.{table}"
)

st.divider()

# ============================================================
# TABLE STATISTICS
# ============================================================

rows = get_table_count(
    schema,
    table,
)

columns = get_columns(
    schema,
    table,
)

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Rows",
        f"{rows:,}"
    )

with c2:

    st.metric(
        "Columns",
        len(columns)
    )

st.divider()

# ============================================================
# COLUMN METADATA
# ============================================================

st.header("📋 Column Metadata")

st.dataframe(
    columns,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ============================================================
# TABLE PREVIEW
# ============================================================

st.header("👀 Table Preview")

preview = preview_table(
    schema,
    table,
    20,
)

st.dataframe(
    preview,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ============================================================
# SQL QUERY RUNNER
# ============================================================

st.header("📝 SQL Query Runner")

default_sql = f"""
SELECT *
FROM {schema}.{table}
LIMIT 20;
"""

query = st.text_area(
    "SQL",
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

# ============================================================
# DATABASE OBJECTS
# ============================================================

st.header("ℹ Database Information")

left, right = st.columns(2)

with left:

    st.markdown(f"""
### Connection

- **Database Size:** {database_size}
- **Schemas:** {schema_count}
- **Tables:** {tables_count}
- **Views:** {views_count}
- **Indexes:** {indexes_count}
""")

with right:

    st.markdown("""
### Project Architecture

- PostgreSQL Operational Database
- Staging Layer
- Analytics Layer
- dbt Transformations
- Google BigQuery
- Streamlit Dashboard
""")

st.divider()

st.success("✅ PostgreSQL Explorer Loaded Successfully")