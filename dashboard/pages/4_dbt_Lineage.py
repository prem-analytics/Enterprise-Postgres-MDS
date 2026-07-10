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

from services.sql_analyzer import (
    analyze_sql,
    complexity_score,
)

from streamlit_agraph import (
    Node,
    Edge,
    Config,
    agraph,
)

from services.dbt_service import (
    get_project_summary,
    get_models,
    get_model_health,
    get_model_details,
    get_model_dependencies,
    get_downstream_models,
    get_lineage_graph,
    get_model_metadata,
    get_model_sql,
    get_sql_quality,
    get_documentation_coverage,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="dbt Lineage",
    page_icon="🌳",
    layout="wide",
)

st.title("🌳 Enterprise dbt Lineage Dashboard")

st.markdown("""
Explore dbt models, metadata, and lineage for PostgreSQL and BigQuery projects.
""")

st.divider()

# ==========================================================
# PROJECT SELECTOR
# ==========================================================

project = st.selectbox(
    "Select dbt Project",
    [
        "postgres",
        "bigquery",
    ],
)

summary = get_project_summary(project)
models = get_models(project)
docs = get_documentation_coverage(project)

# ==========================================================
# PROJECT KPIs
# ==========================================================

st.header("📦 Project Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Models", summary["Models"])

with c2:
    st.metric("Sources", summary["Sources"])

with c3:
    st.metric("Tests", summary["Tests"])

with c4:
    st.metric("Macros", summary["Macros"])

st.divider()

# ==========================================================
# DOCUMENTATION COVERAGE
# ==========================================================

st.header("📚 Documentation Coverage")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Coverage",
        f"{docs['Coverage']}%"
    )

with c2:
    st.metric(
        "Descriptions",
        docs["Documented"]
    )

with c3:
    st.metric(
        "Missing",
        docs["Missing"]
    )

st.progress(
    docs["Coverage"] / 100
)

if docs["Coverage"] >= 90:
    st.success("Excellent documentation coverage.")

elif docs["Coverage"] >= 70:
    st.info("Good documentation coverage.")

elif docs["Coverage"] >= 50:
    st.warning("Documentation should be improved.")

else:
    st.error("Poor documentation coverage.")

# ==========================================================
# MODEL EXPLORER
# ==========================================================

st.header("📂 Model Explorer")

search = st.text_input(
    "🔍 Search Model",
    placeholder="Type model name..."
)

materialization = st.selectbox(
    "Materialization",
    ["All"] + sorted(models["Materialization"].dropna().unique().tolist())
)

schema = st.selectbox(
    "Schema",
    ["All"] + sorted(models["Schema"].dropna().unique().tolist())
)

filtered = models.copy()

if search:
    filtered = filtered[
        filtered["Model"].str.contains(search, case=False)
    ]

if materialization != "All":
    filtered = filtered[
        filtered["Materialization"] == materialization
    ]

if schema != "All":
    filtered = filtered[
        filtered["Schema"] == schema
    ]

st.success(
    f"Showing {len(filtered)} of {len(models)} models"
)

st.dataframe(
    filtered,
    width="stretch",
    hide_index=True,
)

st.divider()

# ==========================================================
# MODEL HEALTH DASHBOARD
# ==========================================================

st.header("💚 Model Health Dashboard")

views = len(
    filtered[
        filtered["Materialization"] == "view"
    ]
)

tables = len(
    filtered[
        filtered["Materialization"] == "table"
    ]
)

others = len(filtered) - views - tables

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Total Models",
        len(filtered)
    )

with c2:
    st.metric(
        "🔵 Views",
        views
    )

with c3:
    st.metric(
        "🟢 Tables",
        tables
    )

with c4:
    st.metric(
        "⚪ Others",
        others
    )

st.progress(
    len(filtered) / max(len(models), 1)
)

st.success(
    f"{len(filtered)} models currently visible."
)

st.divider()

st.header("📊 Model Analytics")

left, right = st.columns(2)

# Materialization chart
with left:

    materialization_df = (
        filtered["Materialization"]
        .value_counts()
        .reset_index()
    )

    materialization_df.columns = [
        "Materialization",
        "Count",
    ]

    fig = px.pie(
        materialization_df,
        names="Materialization",
        values="Count",
        title="Materialization Distribution",
        hole=0.45,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

# Schema chart
with right:

    schema_df = (
        filtered["Schema"]
        .value_counts()
        .reset_index()
    )

    schema_df.columns = [
        "Schema",
        "Count",
    ]

    fig = px.bar(
        schema_df,
        x="Schema",
        y="Count",
        text="Count",
        title="Models by Schema",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

# ==========================================================
# MODEL DETAILS
# ==========================================================

# ==========================================================
# SEARCH MODEL
# ==========================================================

st.header("🔍 Search Model")

selected_model = st.selectbox(
    "Choose a dbt Model",
    models["Model"].tolist()
)

details = get_model_details(
    selected_model,
    project,
)

metadata = get_model_metadata(
    selected_model,
    project,
)

sql = get_model_sql(
    selected_model,
    project,
)

st.header("📋 Selected Model Details")

left, right = st.columns(2)

with left:

    st.metric("Model", details["name"])

    st.metric(
        "Materialization",
        details["config"].get("materialized", "-")
    )

    st.metric(
        "Schema",
        details.get("schema", "-")
    )

with right:

    st.metric(
        "Database",
        details.get("database", "-")
    )

    st.metric(
        "Package",
        details.get("package_name", "-")
    )

st.markdown("### Description")

st.info(
    details.get(
        "description",
        "No description available."
    )
)

st.divider()

# ==========================================================
# MODEL LINEAGE
# ==========================================================

st.header("🌲 Model Lineage")

upstream = get_model_dependencies(
    selected_model,
    project,
)

downstream = get_downstream_models(
    selected_model,
    project,
)

# ==========================================================
# DEPENDENCY SUMMARY
# ==========================================================

st.subheader("📊 Dependency Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "⬆ Upstream",
        len(upstream)
    )

with c2:
    st.metric(
        "⬇ Downstream",
        len(downstream)
    )

with c3:
    st.metric(
        "🔗 Total Connections",
        len(upstream) + len(downstream)
    )

if len(upstream) + len(downstream) == 0:

    st.info("Independent model")

elif len(downstream) == 0:

    st.warning("Terminal model (Final Model)")

elif len(upstream) == 0:

    st.success("Root Model")

else:

    st.success("Intermediate Transformation Model")

left, right = st.columns(2)

with left:

    st.subheader("⬆ Upstream Dependencies")

    if upstream:

        for model in upstream:

            st.success(model)

    else:

        st.info("No upstream dependencies.")

with right:

    st.subheader("⬇ Downstream Models")

    if downstream:

        for model in downstream:

            st.success(model)

    else:

        st.info("No downstream models.")

st.divider()

st.subheader("📑 Enterprise Metadata Card")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Package",
        metadata["Package"]
    )

    st.metric(
        "Schema",
        metadata["Schema"]
    )

    st.metric(
        "Database",
        metadata["Database"]
    )

    st.metric(
        "Materialization",
        metadata["Materialization"]
    )

with c2:

    st.metric(
        "Alias",
        metadata["Alias"] or "-"
    )

    st.metric(
        "Tags",
        metadata["Tags"] or "-"
    )

st.markdown("### 📁 SQL File")

st.code(
    metadata["Path"],
    language="text"
)

st.markdown("### 💻 SQL Preview")

if sql:

    st.code(
        sql,
        language="sql"
    )

else:

    st.warning(
        "SQL file not found."
    )
# ==========================================================
# SQL ANALYTICS
# ==========================================================

if sql:

    st.divider()

    st.header("📊 SQL Analytics")

    stats = analyze_sql(sql)

    score, level = complexity_score(stats)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Lines", stats["Lines"])

    with c2:
        st.metric("🔍 SELECT", stats["SELECT"])

    with c3:
        st.metric("🔗 JOIN", stats["JOIN"])

    with c4:
        st.metric("🧩 CASE", stats["CASE"])

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.metric("📦 WITH", stats["WITH"])

    with c6:
        st.metric("📚 GROUP BY", stats["GROUP BY"])

    with c7:
        st.metric("↔ UNION", stats["UNION"])

    with c8:
        st.metric("📍 ref()", stats["REF"])
    
    st.divider()

    st.subheader("🚦 SQL Complexity")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Complexity Score",
            score
        )

    with c2:
        st.metric(
            "Level",
            level
        )

    if "Low" in level:
        st.success("Simple model with low maintenance cost.")

    elif "Medium" in level:
        st.info("Moderate complexity. Easy to maintain.")

    elif "High" in level:
        st.warning("High complexity. Consider reviewing joins and transformations.")

    else:
        st.error("Very complex model. Optimization recommended.")
# ==========================================================
# SQL QUALITY REPORT
# ==========================================================

st.divider()

st.header("✅ SQL Quality Report")

quality = get_sql_quality(
    details,
    sql,
    stats
)

st.dataframe(
    quality,
    hide_index=True,
    width="stretch",
)

# ==========================================================
# INTERACTIVE GRAPH
# ==========================================================

st.divider()

st.header("🌐 Interactive dbt Lineage Graph")

nodes_data, edges_data = get_lineage_graph(project)

nodes = []

for node in nodes_data:

    if node["type"] == "source":

        color = "#F39C12"
        shape = "database"

    else:

        if node["materialized"] == "view":
            color = "#3498DB"

        else:
            color = "#2ECC71"

        shape = "box"

    nodes.append(

        Node(

            id=node["id"],

            label=node["label"],

            size=30,

            color=color,

            shape=shape,

            font={

                "size":16,

                "face":"Arial",

                "color":"black",

            },

            title=f"""
        <b>{node['label']}</b>

        Materialization:
        {node['materialized']}

        Schema:
        {node.get('schema','')}

        Database:
        {node.get('database','')}

        Description:
        {node.get('description','No description')}
        """,

    )

    )

edges = []

for edge in edges_data:

    edges.append(

        Edge(

            source=edge["source"],

            target=edge["target"],

            smooth=True,

            color="#555555",
            width=3,

        )

    )

config = Config(

    width=1200,
    height=750,

    directed=True,

    physics=False,

    hierarchical=True,

    nodeHighlightBehavior=True,

    highlightColor="#F7A7A6",

    collapsible=True,

    layout={

        "hierarchical": {

            "enabled": True,

            "direction": "UD",

            "sortMethod": "directed",

            "levelSeparation": 250,

            "nodeSpacing": 260,

        }

    }

)

st.info("""
🟠 Source Tables

🔵 Staging Models

🟢 Fact / Mart Models
""")

agraph(
    nodes=nodes,
    edges=edges,
    config=config,
)