from services.dbt_service import *

print("=" * 60)
print("POSTGRES DBT")
print("=" * 60)

print(get_project_summary("postgres"))

print(get_models("postgres").head())

print(get_model_dependencies(
    "fct_user_post_metrics",
    "postgres"
))

print()

print("=" * 60)
print("BIGQUERY DBT")
print("=" * 60)

print(get_project_summary("bigquery"))

print(get_models("bigquery").head())

print(get_model_dependencies(
    "fct_orders",
    "bigquery"
))