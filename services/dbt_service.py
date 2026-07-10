import json
import os
import pandas as pd

# ==========================================================
# dbt Artifact Paths
# ==========================================================

POSTGRES_MANIFEST = os.path.join(
    "postgres_pipeline",
    "target",
    "manifest.json"
)

BIGQUERY_MANIFEST = os.path.join(
    "enterprise-bigquery-mds",
    "bigquery_pipeline",
    "target",
    "manifest.json"
)


# ==========================================================
# Load Manifest
# ==========================================================

def load_manifest(project="postgres"):

    if project == "postgres":
        path = POSTGRES_MANIFEST

    elif project == "bigquery":
        path = BIGQUERY_MANIFEST

    else:
        raise ValueError("Invalid project name")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Manifest not found:\n{path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# Project Summary
# ==========================================================

def get_project_summary(project="postgres"):

    manifest = load_manifest(project)

    models = 0
    tests = 0
    snapshots = 0
    seeds = 0

    for node in manifest["nodes"].values():

        resource = node["resource_type"]

        if resource == "model":
            models += 1

        elif resource == "test":
            tests += 1

        elif resource == "snapshot":
            snapshots += 1

        elif resource == "seed":
            seeds += 1

    return {

        "Models": models,

        "Sources": len(
            manifest.get("sources", {})
        ),

        "Tests": tests,

        "Seeds": seeds,

        "Snapshots": snapshots,

        "Macros": len(
            manifest.get("macros", {})
        ),

        "Exposures": len(
            manifest.get("exposures", {})
        ),

        "Metrics": len(
            manifest.get("metrics", {})
        ),

        "Groups": len(
            manifest.get("groups", {})
        ),
    }


# ==========================================================
# Model Explorer
# ==========================================================

def get_models(project="postgres"):

    manifest = load_manifest(project)

    rows = []

    for node in manifest["nodes"].values():

        if node["resource_type"] != "model":
            continue

        rows.append({

            "Model": node.get("name"),

            "Schema": node.get("schema"),

            "Database": node.get("database"),

            "Materialization": node["config"].get(
                "materialized"
            ),

            "Package": node.get(
                "package_name"
            ),

            "Description": node.get(
                "description"
            ),

        })

    return pd.DataFrame(rows)


# ==========================================================
# Single Model Details
# ==========================================================

def get_model_details(model_name, project="postgres"):

    manifest = load_manifest(project)

    for node in manifest["nodes"].values():

        if (
            node["resource_type"] == "model"
            and node["name"] == model_name
        ):

            return node

    return None


# ==========================================================
# Upstream Dependencies
# ==========================================================

def get_model_dependencies(model_name, project="postgres"):

    manifest = load_manifest(project)

    for node in manifest["nodes"].values():

        if (
            node["resource_type"] == "model"
            and node["name"] == model_name
        ):

            return node.get(
                "depends_on",
                {}
            ).get(
                "nodes",
                []
            )

    return []


# ==========================================================
# Downstream Dependencies
# ==========================================================

def get_downstream_models(model_name, project="postgres"):

    manifest = load_manifest(project)

    downstream = []

    for node in manifest["nodes"].values():

        if node["resource_type"] != "model":
            continue

        deps = node.get(
            "depends_on",
            {}
        ).get(
            "nodes",
            []
        )

        for dep in deps:

            if dep.endswith(model_name):

                downstream.append(
                    node["name"]
                )

    return downstream
# ==========================================================
# Interactive Lineage Graph
# ==========================================================

def get_lineage_graph(project):

    manifest = load_manifest(project)

    graph_nodes = []
    graph_edges = []

    added = set()

    # -----------------------------
    # Add model nodes
    # -----------------------------

    for node_id, node in manifest["nodes"].items():

        if node["resource_type"] != "model":
            continue

        model = node["name"]

        if model not in added:

            graph_nodes.append({

                "id": model,

                "label": model,

                "type": "model",

                "materialized": node["config"].get(
                    "materialized",
                    "table"
                ),

                "schema": node.get("schema", ""),

                "database": node.get("database", ""),

                "description": node.get("description", ""),

            })

    # -----------------------------
    # Add source nodes
    # -----------------------------

    for source_id, source in manifest.get(
        "sources",
        {}
    ).items():

        source_name = source["name"]

        if source_name not in added:

            graph_nodes.append({

                "id": source_name,

                "label": source_name,

                "type": "source",

                "materialized": "source"

            })

            added.add(source_name)

    # -----------------------------
    # Add dependencies
    # -----------------------------

    for node_id, node in manifest["nodes"].items():

        if node["resource_type"] != "model":
            continue

        current = node["name"]

        deps = node.get(
            "depends_on",
            {}
        ).get(
            "nodes",
            []
        )

        for dep in deps:

            if dep in manifest["nodes"]:

                parent = manifest["nodes"][dep]["name"]

            elif dep in manifest.get("sources", {}):

                parent = manifest["sources"][dep]["name"]

            else:

                continue

            graph_edges.append({

                "source": parent,

                "target": current

            })

    return graph_nodes, graph_edges

# ==========================================================
# Model Health Dashboard
# ==========================================================

def get_model_health(project):

    models = get_models(project)

    rows = []

    for _, row in models.iterrows():

        name = row["Model"]

        upstream = len(
            get_model_dependencies(
                name,
                project
            )
        )

        downstream = len(
            get_downstream_models(
                name,
                project
            )
        )

        status = "🟢 Healthy"

        rows.append({

            "Model": name,

            "Materialization": row["Materialization"],

            "Upstream": upstream,

            "Downstream": downstream,

            "Status": status,

        })

    return pd.DataFrame(rows)
# ==========================================================
# Metadata Card
# ==========================================================

def get_model_metadata(model_name, project):

    details = get_model_details(model_name, project)

    return {
        "Model": details.get("name", ""),
        "Package": details.get("package_name", ""),
        "Database": details.get("database", ""),
        "Schema": details.get("schema", ""),
        "Alias": details.get("alias", ""),
        "Materialization": details.get("config", {}).get("materialized", ""),
        "Description": details.get("description", ""),
        "Path": details.get("original_file_path", ""),
        "Tags": ", ".join(details.get("tags", [])),
    }
# ==========================================================
# Read SQL File
# ==========================================================

def get_model_sql(model_name, project):

    details = get_model_details(model_name, project)

    if not details:
        return None

    path = details.get("original_file_path")

    if not path:
        return None

    if project == "postgres":
        sql_path = os.path.join("postgres_pipeline", path)
    else:
        sql_path = os.path.join(
            "enterprise-bigquery-mds",
            "bigquery_pipeline",
            path,
        )

    if not os.path.exists(sql_path):
        return None

    with open(sql_path, "r", encoding="utf-8") as f:
        return f.read()
# ==========================================================
# SQL Quality Report
# ==========================================================

def get_sql_quality(details, sql, stats):

    checks = []

    # Description
    if details.get("description"):
        checks.append(("✅ Description", "Present"))
    else:
        checks.append(("❌ Description", "Missing"))

    # Tags
    if details.get("tags"):
        checks.append(("✅ Tags", "Present"))
    else:
        checks.append(("⚠ Tags", "Missing"))

    # ref()
    if stats["REF"] > 0:
        checks.append(("✅ dbt ref()", f"{stats['REF']} used"))
    else:
        checks.append(("❌ dbt ref()", "None"))

    # WITH
    if stats["WITH"] > 0:
        checks.append(("✅ CTE", "Uses WITH"))
    else:
        checks.append(("⚠ CTE", "No WITH clause"))

    # JOINS
    if stats["JOIN"] <= 3:
        checks.append(("✅ JOIN Count", str(stats["JOIN"])))
    else:
        checks.append(("⚠ JOIN Count", str(stats["JOIN"])))

    # CASE
    if stats["CASE"] <= 5:
        checks.append(("✅ CASE Statements", str(stats["CASE"])))
    else:
        checks.append(("⚠ CASE Statements", str(stats["CASE"])))

    # Length
    if stats["Lines"] < 150:
        checks.append(("✅ SQL Length", f"{stats['Lines']} lines"))
    else:
        checks.append(("⚠ SQL Length", f"{stats['Lines']} lines"))

    df = pd.DataFrame(
        checks,
        columns=[
            "Check",
            "Result"
        ]
    )

    df["Result"] = df["Result"].astype(str)

    return df

# ==========================================================
# Documentation Coverage
# ==========================================================

def get_documentation_coverage(project):

    models = get_models(project)

    total = len(models)

    documented = models["Description"].fillna("").str.strip().ne("").sum()

    missing = total - documented

    coverage = round(
        documented / max(total, 1) * 100,
        1
    )

    return {
        "Total": total,
        "Documented": documented,
        "Missing": missing,
        "Coverage": coverage,
    }
# ==========================================================
# Documentation Coverage
# ==========================================================

def get_documentation_coverage(project):

    models = get_models(project)

    total = len(models)

    documented = models["Description"].fillna("").str.strip().ne("").sum()

    missing = total - documented

    coverage = round(
        documented / max(total, 1) * 100,
        1
    )

    return {
        "Total": total,
        "Documented": documented,
        "Missing": missing,
        "Coverage": coverage,
    }    