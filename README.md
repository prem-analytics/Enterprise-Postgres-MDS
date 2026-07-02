# 📊 Enterprise Modern Data Stack (MDS) Pipeline

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-app-mds-aclgz2gmz7bfiyvsygnmre.streamlit.app)

An end-to-end analytics engineering platform orchestrating data ingestion, warehouse transformation, automated data quality testing, and interactive reporting using a secure, credential-decoupled architecture.

## 🏗️ Architecture Overview

The platform implements a complete automated data lifecycle split across five distinct layers:

1. **Ingestion Layer (Python):** Connects to a REST API endpoint to extract raw platform data and stream it via buffered transactional queries into a database staging layer. Features a randomized sliding-window data generator to simulate live, continuous delta updates.
2. **Orchestration Layer (Dagster):** Serves as the control plane pipeline engine, mapping functional dependencies asset-by-asset with visual tracking planes.
3. **Storage & Warehousing (PostgreSQL 18):** Hosts isolated transaction-safe database schemas split across `staging` (raw entry landing) and `analytics` (downstream consumption metrics).
4. **Transformation & Testing Framework (dbt Core):** Rebuilds materializations using modular SQL design patterns while strictly executing embedded data quality constraints to ensure primary keys remain `unique` and `not_null`.
5. **Business Intelligence Layer (Streamlit & Plotly):** Extends deep visibility to business stakeholders by running sub-second analytical aggregations mapped directly to interactive web dashboards.

## 🛠️ Tech Stack Matrix

* **Orchestration & Data Lineage:** Dagster Core & Webserver
* **Data Transformation Modeling:** dbt Core (v1.11+)
* **Database & Storage Warehouse:** PostgreSQL 18
* **Frontend Visualization Web Interface:** Streamlit Engine
* **Graphical Analytical Framework:** Plotly Express
* **Programming Core Language:** Python 3.12 (Virtual Environment Isolated)
* **Configuration & Security Management:** Python-Dotenv / Os Environment Keyrings

## 🛡️ Enterprise Security Configuration

To ensure production compliance and make the codebase safe for public repositories, all operational parameters have been extracted out of cleartext files and decoupled using an environment configuration layer.

Database connections are securely injected at runtime using Jinja context expressions within dbt:
```yaml
host: "{{ env_var('DB_HOST') }}"
user: "{{ env_var('DB_USER') }}"
password: "{{ env_var('DB_PASSWORD') }}"