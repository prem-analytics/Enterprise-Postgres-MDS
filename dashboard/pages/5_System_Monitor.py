import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="System Monitor",
    page_icon="🖥",
    layout="wide"
)

st.title("🖥 Enterprise System Monitor")

st.write(
    "Monitor the health of the Modern Data Stack."
)

st.divider()

# ============================================================
# PLATFORM STATUS
# ============================================================

st.header("Platform Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "PostgreSQL",
        "🟢 Online"
    )

with c2:
    st.metric(
        "BigQuery",
        "🟢 Online"
    )

with c3:
    st.metric(
        "dbt",
        "🟢 Ready"
    )

with c4:
    st.metric(
        "Dagster",
        "🟢 Running"
    )

st.divider()

# ============================================================
# PIPELINE HEALTH
# ============================================================

st.header("Pipeline Health")

health = pd.DataFrame({

    "Pipeline":[
        "REST API Ingestion",
        "PostgreSQL Load",
        "dbt Transformation",
        "BigQuery Load",
        "Dashboard Refresh"
    ],

    "Status":[
        "Success",
        "Success",
        "Success",
        "Success",
        "Success"
    ],

    "Duration":[
        "45 sec",
        "12 sec",
        "28 sec",
        "18 sec",
        "3 sec"
    ],

    "Last Run":[
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ]

})

st.dataframe(
    health,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# SYSTEM METRICS
# ============================================================

st.header("System Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "CPU Usage",
    "32%"
)

m2.metric(
    "Memory",
    "4.8 GB"
)

m3.metric(
    "Disk Usage",
    "45%"
)

m4.metric(
    "Network",
    "Healthy"
)

st.divider()

# ============================================================
# RECENT LOGS
# ============================================================

st.header("Recent Logs")

logs = pd.DataFrame({

    "Time":[
        "10:02",
        "10:04",
        "10:05",
        "10:06",
        "10:07"
    ],

    "Service":[
        "PostgreSQL",
        "dbt",
        "BigQuery",
        "Dagster",
        "Dashboard"
    ],

    "Level":[
        "INFO",
        "INFO",
        "INFO",
        "INFO",
        "INFO"
    ],

    "Message":[
        "Database connected",
        "Models executed successfully",
        "Warehouse updated",
        "Pipeline completed",
        "Dashboard refreshed"
    ]

})

st.dataframe(
    logs,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# ALERTS
# ============================================================

st.header("Alerts")

st.success("No active alerts.")

st.success("No failed pipelines.")

st.success("No database connectivity issues.")

st.success("No data quality issues detected.")

st.divider()

# ============================================================
# SYSTEM INFORMATION
# ============================================================

st.header("Environment")

left, right = st.columns(2)

with left:

    st.markdown("""
### Application

- Enterprise Modern Data Stack
- Version 1.0
- Development Environment
- Streamlit Dashboard
""")

with right:

    st.markdown("""
### Stack

- Python
- PostgreSQL
- Google BigQuery
- dbt Core
- Dagster
""")