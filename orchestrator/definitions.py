import os
from pathlib import Path
from dagster import Definitions
from dagster_dbt import DbtProject, dbt_assets, DbtCliResource
from .assets import bq_raw_data_ingestion

# Point dynamically to your clean dbt project directory
DBT_PROJECT_DIR = Path("D:/Enterprise-Postgres-MDS/enterprise-bigquery-mds/bigquery_pipeline")

dbt_project = DbtProject(
    project_dir=os.fspath(DBT_PROJECT_DIR),
)
# Generates or reads your manifest file instantly on startup
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def bq_dbt_assets(context, dbt: DbtCliResource):
    # Runs 'dbt build' which handles running models AND testing data constraints automatically
    yield from dbt.cli(["build"], context=context).stream()

definitions = Definitions(
    assets=[bq_raw_data_ingestion, bq_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
)