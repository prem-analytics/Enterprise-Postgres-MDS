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
import plotly.express as px

from config.config import (
    PROJECT_ID,
    BIGQUERY_DATASET,
)

from services.bigquery_service import (
    get_tables,
    get_row_count,
    get_columns,
    preview_table,
    get_dataset_statistics,
    get_null_statistics,
    get_duplicate_rows,
    get_quality_score,
    get_distinct_values,
    get_numeric_summary,
    run_sql,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Data Quality",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Enterprise Data Quality Dashboard")

st.markdown(
"""
Monitor and profile data quality across your BigQuery warehouse.
"""
)

st.divider()

# ==========================================================
# LOAD TABLES
# ==========================================================

tables_df = get_tables()

table_list = tables_df["table_name"].tolist()

selected_table = st.selectbox(
    "Select BigQuery Table",
    table_list,
)

# ==========================================================
# LOAD METRICS
# ==========================================================

row_count = get_row_count(selected_table)

column_df = get_columns(selected_table)

column_count = len(column_df)

quality_score = get_quality_score(selected_table)

duplicate_rows = get_duplicate_rows(selected_table)

dataset_tables = int(
    get_dataset_statistics()["tables"][0]
)

# ==========================================================
# OVERVIEW KPI
# ==========================================================

st.header("🏢 Warehouse Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Project",
        PROJECT_ID,
    )

with c2:
    st.metric(
        "Dataset",
        BIGQUERY_DATASET,
    )

with c3:
    st.metric(
        "Tables",
        dataset_tables,
    )

with c4:
    st.metric(
        "Selected Table",
        selected_table,
    )

st.divider()

# ==========================================================
# TABLE KPI
# ==========================================================

st.header("📈 Data Quality KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Rows",
        f"{row_count:,}"
    )

with k2:
    st.metric(
        "Columns",
        column_count
    )

with k3:
    st.metric(
        "Duplicate Rows",
        duplicate_rows
    )

with k4:
    st.metric(
        "Quality Score",
        f"{quality_score:.2f}%"
    )

st.divider()

# ==========================================================
# QUALITY SCORE
# ==========================================================

st.header("🎯 Overall Data Quality")

score_color = (
    "green"
    if quality_score >= 95
    else "orange"
    if quality_score >= 80
    else "red"
)

st.progress(quality_score / 100)

st.success(
    f"Overall Data Quality Score : {quality_score:.2f}%"
)

st.divider()

# ==========================================================
# NULL ANALYSIS
# ==========================================================

st.header("📊 Null Value Analysis")

null_df = get_null_statistics(selected_table)

left, right = st.columns([2,3])

with left:

    st.dataframe(
        null_df,
        use_container_width=True,
        hide_index=True,
    )

with right:

    fig = px.bar(
        null_df,
        x="Column",
        y="Null Count",
        color="Null %",
        text="Null Count",
        title="Null Values by Column",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# COLUMN METADATA
# ==========================================================

st.header("📋 Column Metadata")

st.dataframe(
    column_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# DISTINCT VALUES
# ==========================================================

st.header("🔢 Distinct Values")

distinct_df = get_distinct_values(
    selected_table
)

left, right = st.columns([2,3])

with left:

    st.dataframe(
        distinct_df,
        use_container_width=True,
        hide_index=True,
    )

with right:

    fig = px.bar(
        distinct_df,
        x="Column",
        y="Distinct Values",
        text="Distinct Values",
        color="Distinct Values",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# NUMERIC PROFILE
# ==========================================================

st.header("📈 Numeric Profile")

try:

    numeric = get_numeric_summary(
        selected_table
    )

    st.dataframe(
        numeric,
        use_container_width=True,
    )

except Exception:

    st.info(
        "No numeric columns available."
    )

st.divider()

st.header("👀 Data Preview")

preview = preview_table(
    selected_table,
    limit=20
)

preview = preview.copy()

for col in preview.columns:

    if preview[col].dtype == "object":
        preview[col] = preview[col].astype(str)

st.dataframe(
    preview,
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.header("💻 SQL Query Runner")

sql = st.text_area(

    "Write SQL",

    value=f"""
SELECT *
FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{selected_table}`
LIMIT 20
""",

    height=180

)

if st.button("Execute SQL"):

    try:

        result = run_sql(sql)

        st.success("Query executed successfully.")

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
        )

    except Exception as e:

        st.error(e)

st.divider()

st.header("🎯 Automatic Quality Recommendations")

if quality_score >= 98:

    st.success(
        "Excellent dataset. No major quality issues detected."
    )

elif quality_score >= 90:

    st.warning(
        "Dataset quality is good. Review nullable columns."
    )

else:

    st.error(
        "Data quality requires attention."
    )

if duplicate_rows > 0:

    st.warning(
        f"{duplicate_rows} duplicate rows detected."
    )

else:

    st.success(
        "No duplicate rows detected."
    )

if null_df["Null Count"].sum() == 0:

    st.success(
        "No missing values detected."
    )

else:

    st.warning(
        "Missing values exist."
    )

st.divider()

st.header("📈 Data Distribution")

numeric_cols = preview.select_dtypes(
    include="number"
).columns

if len(numeric_cols):

    selected_numeric = st.selectbox(

        "Numeric Column",

        numeric_cols

    )

    fig = px.histogram(

        preview,

        x=selected_numeric,

        nbins=20,

        title=f"Distribution of {selected_numeric}"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

else:

    st.info(
        "No numeric columns available."
    )

st.divider()

st.header("🏁 Dashboard Summary")

left, right = st.columns(2)

with left:

    st.markdown("""
### Completed Checks

- ✅ Null Analysis
- ✅ Duplicate Analysis
- ✅ Metadata Inspection
- ✅ Distinct Values
- ✅ Numeric Profiling
- ✅ SQL Runner
- ✅ Data Preview
""")

with right:

    st.metric(
        "Overall Score",
        f"{quality_score:.2f}%"
    )

    st.metric(
        "Tables",
        dataset_tables
    )

    st.metric(
        "Rows",
        row_count
    )

    st.metric(
        "Columns",
        column_count
    )

