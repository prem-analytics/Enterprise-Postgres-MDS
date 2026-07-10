Markdown
# 📊 Enterprise Modern Data Stack (MDS)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-app-mds-aclgz2gmz7bfiyvsygnmre.streamlit.app)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![dbt Core](https://img.shields.io/badge/dbt-Core%20v1.8+-orange.svg)](https://www.getdbt.com/)
[![Dagster](https://img.shields.io/badge/orchestration-Dagster-purple.svg)](https://dagster.io/)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql)
![BigQuery](https://img.shields.io/badge/Google_BigQuery-Analytics-4285F4?logo=googlebigquery)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-4285F4?logo=googlecloud)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-black?logo=github)
![MIT License](https://img.shields.io/badge/License-MIT-green)

An end-to-end, production-grade Modern Data Stack platform implementing cloud-native analytics engineering practices. The project automates data ingestion from third-party REST APIs, stores analytical datasets in Google BigQuery, models business-ready data using dbt Core, orchestrates workflows with Dagster, and delivers interactive business intelligence dashboards through Streamlit. PostgreSQL serves as the relational analytics environment for SQL development and downstream data modeling.

---

## 🏗️ Reference Architecture & Pipeline Execution Layers

The framework organizes complex workflows into six decoupled execution layers to enforce separation of concerns, data integrity tracking, and strict system scalability.



### 1️⃣ Ingestion Layer (Python Engine)
* **Decoupled Extraction:** Orchestrates custom Python modules targeting external production REST API endpoints.
* **Fault-Tolerant Patterns:** Standardizes robust execution routines including stateful cursor incremental extraction, programmatic token renewal loops, dynamic page offset handling, and exponential backoff retry algorithms to handle network exceptions.

### 2️⃣ Raw Cloud Storage Zone (Google BigQuery Warehouse)
* **Central Data Lakehouse:** Serves as the immutable raw historical repository.
* **Scale-Out Compute:** Stores untransformed API responses directly inside cost-optimized BigQuery tables, utilizing massive parallel processing (MPP) capabilities to support heavy historical aggregations.
* **Namespaces:** Tracks source state across isolated `raw` landing datasets and polished `analytics` marts.

### 3️⃣ Relational Analytics Layer (PostgreSQL)

PostgreSQL serves as the relational analytics database within the Modern Data Stack.

**Responsibilities**

- Stores structured analytical datasets.
- Supports dbt transformations and modeling.
- Provides a relational environment for SQL development and testing.
- Acts as the operational analytics database for downstream reporting.

**Schemas**

```text
staging
analytics
```

### 4️⃣ Transformation & Data Quality Engineering (dbt Core™)
* **Idempotent Data Modeling:** Transforms raw staging entries into analytical schemas using modular SQL structures.
* **Performance Optimization:** Employs optimal table virtualization patterns by building critical analytical components as high-performance materializations (incremental models, views, and optimized tables).
* **Automated Quality Guardrails:** Implements automated data asset validation tests ensuring strict compliance with system keys and entity constraints:
    * `unique` and `not_null` key validation checks.
    * `accepted_values` domain enforcement.
    * `relationships` check for referential integrity across dimensions and facts.

### 5️⃣ Pipeline Orchestration & Asset Management (Dagster)
* **Declarative Control Plane:** Coordinates the complete execution lifecycle using an asset-based orchestration model.
* **Operational Visibility:** Manages deep parent-child step dependency maps, schedules automated window runs, tracks system exceptions, and captures structural execution metadata for end-to-end lineage tracking.

### 6️⃣ Enterprise Business Intelligence Layer (Streamlit & Plotly)
* **Dynamic Data Delivery:** Renders real-time executive-level performance insights via a modern dashboard.
* **Low-Latency Interactivity:** Couples Plotly visualization frames directly to cached database query wrappers to display high-level platform health metrics without executing costly redundant backend warehouse scans.

---

## 🔄 End-to-End Analytics Lineage

```text
🌐 REST API
      │
      ▼
🐍 Python Ingestion
      │
      ▼
☁️ Google BigQuery
   (Raw Landing Zone)
      │
      ▼
🐘 PostgreSQL
 (Relational Analytics)
      │
      ▼
🟧 dbt Core
 (Models & Tests)
      │
      ▼
🟣 Dagster
 (Pipeline Orchestration)
      │
      ▼
📊 Streamlit Dashboard
```

## ✅ Current Features

- REST API Data Ingestion
- Google BigQuery Cloud Warehouse
- PostgreSQL Relational Database
- dbt Core Data Modeling
- Dagster Pipeline Orchestration
- Streamlit Interactive Dashboard
- Plotly Business Visualizations
- Secure Google Service Account Authentication
- Cloud Deployment using Streamlit Community Cloud

## 🛠️ Integrated Technology Matrix

| Stack Layer | Component Technology | Focus Domain |
|:---|:---|:---|
| **Programming Language** | Python 3.12 | Core Ingestion Logic & Custom ETL Scripts |
| **Cloud Data Warehouse** | Google BigQuery | Scalable Cloud Compute & Large Scale Storage |
| **Relational Store** | PostgreSQL | Highly Indexed Operational Performance Layer |
| **Transformation Engine**| dbt Core (v1.8+) | Analytical SQL Modeling & Automated Asset Testing |
| **Orchestration Control**| Dagster | Declarative Asset-Based Pipeline Dependencies |
| **Presentation Framework**| Streamlit | Interactive Portfolio UI & Component State Capture |
| **Visualization Layer** | Plotly Express | Dynamic Matrix Charts & Distribution Maps |
| **Security Layer** | Google Service Account | Cryptographic IAM Validation & Secret Decoupling |
| **Source Control** | Git & GitHub | Distributed Version Control & Environment Isolation |

---

## 📂 Repository Blueprint

```text
Enterprise-Modern-Data-Stack/
│
├── 📁 config/
│   └── config.py                   # Central application configuration
│
├── 📁 dashboard/
│   ├── dashboard_app.py            # Streamlit analytics dashboard
│   ├── README.md
│   ├── assets/                     # CSS, icons, images
│   └── pages/                      # Multi-page Streamlit apps
│
├── 📁 docs/
│   ├── Architecture.md
│   ├── BigQuery.md
│   ├── PostgreSQL.md
│   ├── DataFlow.md
│   └── Deployment.md
│
├── 📁 images/
│   ├── architecture.png
│   └── dashboard.png
│
├── 📁 ingestion/
│   ├── ingest_to_postgres.py
│   ├── api_client.py
│   ├── validation.py
│   ├── utils.py
│   └── README.md
│
├── 📁 services/
│   ├── bigquery_service.py         # BigQuery operations
│   ├── postgres_service.py         # PostgreSQL operations
│   └── README.md
│
├── 📁 pipelines/
│   ├── bigquery_pipeline/
│   ├── postgres_pipeline/
│   └── README.md
│
├── 📁 orchestrator/
│   ├── assets.py
│   ├── jobs.py
│   ├── schedules.py
│   └── README.md
│
├── 📁 postgres_pipeline/
│   ├── models/
│   ├── macros/
│   ├── seeds/
│   ├── snapshots/
│   ├── tests/
│   ├── dbt_project.yml
│   ├── packages.yml
│   ├── profiles.yml
│   └── README.md
│
├── 📁 sql/
│   ├── analytics.sql
│   ├── dashboard_queries.sql
│   └── reporting.sql
│
├── 📁 utils/
│   ├── logger.py
│   ├── helpers.py
│   └── constants.py
│
├── 📁 models/
│   ├── customer.py
│   ├── order.py
│   └── payment.py
│
├── 📁 logs/
│   └── README.md
│
├── 📁 tests/
│   ├── README.md
│   ├── test_ingestion.py
│   ├── test_bigquery.py
│   ├── test_postgres.py
│   └── test_dashboard.py
│
├── .env
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```


> **Note:** Some folders and files shown above (such as `assets/`, `pages/`, `api_client.py`, and `validation.py`) are part of the planned project architecture and will be added in future development phases.

## 📦 Project Modules

| Module | Description |
|---------|-------------|
| **Python Ingestion** | Extracts data from external REST APIs using authenticated requests and incremental loading strategies. |
| **Google BigQuery** | Stores raw analytical datasets and serves as the cloud data warehouse. |
| **PostgreSQL** | Provides a relational analytics layer for downstream reporting and SQL-based analysis. |
| **dbt Core** | Transforms raw data into analytics-ready models while performing automated data quality testing. |
| **Dagster** | Orchestrates ingestion, transformation, and reporting workflows with asset-based execution. |
| **Streamlit** | Provides an interactive web dashboard for real-time business intelligence and KPI reporting. |
| **GitHub** | Manages source code, version control, and project documentation. |


## 📈 Project Statistics

| Metric | Value |
|---------|-------|
| Programming Language | Python 3.12 |
| Cloud Platform | Google Cloud Platform |
| Data Warehouse | Google BigQuery |
| Relational Database | PostgreSQL |
| Transformation Tool | dbt Core |
| Orchestration Tool | Dagster |
| Dashboard Framework | Streamlit |
| Visualization Library | Plotly |
| Version Control | Git & GitHub |
| Configuration | Environment Variables (.env) |


## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/<your-username>/Enterprise-Modern-Data-Stack.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run dashboard/dashboard_app.py
```

Launch the Dagster UI:

```bash
dagster dev
```

Run dbt models:

```bash
dbt run
```


## 🚀 Key Architectural Highlights

* **Stateful Incremental Loads:** Bypasses costly full-table overwrites by utilizing timestamp cursors to process only new or modified transaction fields.
* **Self-Healing Configuration Handling:** The Streamlit dashboard includes an authentication engine built to ingest structured TOML profiles, automatically correcting line-break or text-wrapping inconsistencies inside base64 keys.
* **Production Environment Isolation:** Protects all database access vectors by ensuring local key files (`gcp_creds.json`) and system parameters (`.env`) are strictly decoupled from version control branches.

---

## 📈 Dashboard Features

The Streamlit dashboard provides interactive business intelligence through:

- Executive KPI Cards
- Customer Analytics
- Revenue Monitoring
- Order Status Distribution
- Payment Method Analysis
- Interactive Data Tables
- Live BigQuery Analytics

---

## 🔮 Future Enhancements

- BigQuery → PostgreSQL Synchronization
- Docker Containerization
- Terraform Infrastructure as Code (IaC)
- GitHub Actions CI/CD Pipeline
- Great Expectations Data Validation
- Looker Studio Integration
- Automated Monitoring & Alerting
- Data Lineage & Metadata Tracking
- Unit & Integration Testing
- Multi-Environment Deployment (Dev / Test / Prod)

---

## 👨‍💻 Author

**Prem Analytics** *Analytics Engineer & Data Infrastructure Specialist* Specializing in the design, scaling, and automation of robust cloud-native enterprise data stack pipelines. Feel free to connect via GitHub or explore the live dashboard interface!    