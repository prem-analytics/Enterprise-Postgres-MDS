from dagster import AssetExecutionContext, Definitions, asset
from dagster_dbt import DbtCliResource, dbt_assets
import pathlib
import subprocess
import os
from dotenv import load_dotenv # 🌟 ENTERPRISE FIX: Import dotenv loader

# 🌟 ENTERPRISE FIX: Force Dagster to read your secure .env keyring for all sub-processes
load_dotenv(dotenv_path=pathlib.Path(__file__).joinpath("..", "..", ".env").resolve())

# Identify the exact path to our downstream dbt modeling folder
DBT_PROJECT_DIR = pathlib.Path(__file__).joinpath("..", "..", "postgres_pipeline").resolve()

# 🌟 ENTERPRISE FIX: Key name matches what dbt uses inside Definitions
dbt_resource = DbtCliResource(project_dir=os.fspath(DBT_PROJECT_DIR))

@asset(compute_kind="python")
def raw_api_posts_extraction(context: AssetExecutionContext):
    """
    Ingestion Layer: Extracts raw REST API data and loads it securely into PostgreSQL staging tables.
    """
    context.log.info("🚀 Initiating Python core ingestion task...")
    
    # Trigger our verified standalone Python ingestion utility script
    script_path = pathlib.Path(__file__).joinpath("..", "..", "ingest_to_postgres.py").resolve()
    result = subprocess.run(["python", os.fspath(script_path)], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"❌ Ingestion phase failed: {result.stderr}")
    
    context.log.info(f"✅ Ingestion Stream Complete: {result.stdout}")

@dbt_assets(manifest=DBT_PROJECT_DIR.joinpath("target", "manifest.json"))
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    Transformation Layer: Directs dbt Core to execute modular views and relational fact tables.
    """
    yield from dbt.cli(["run"], context=context).stream()

# Bind definitions into a unified execution control plane
defs = Definitions(
    assets=[raw_api_posts_extraction, my_dbt_assets],
    resources={"dbt": dbt_resource}, # 🌟 Maps the resource instance perfectly
)