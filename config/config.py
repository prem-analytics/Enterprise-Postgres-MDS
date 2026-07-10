"""
==========================================================
Enterprise Modern Data Stack
Global Configuration
==========================================================
"""

import os
import streamlit as st
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

PROJECT_NAME = "Enterprise Modern Data Stack"

PROJECT_ID = "analytics-engineering-learning"

# ==========================================================
# GOOGLE BIGQUERY
# ==========================================================

BIGQUERY_DATASET = "analytics"

FACT_TABLE = "fct_orders"

# ==========================================================
# POSTGRESQL
# ==========================================================

try:
    POSTGRES_DB = st.secrets["DB_NAME"]
except Exception:
    POSTGRES_DB = os.getenv("DB_NAME", "")

try:
    POSTGRES_HOST = st.secrets["DB_HOST"]
except Exception:
    POSTGRES_HOST = os.getenv("DB_HOST", "")

try:
    POSTGRES_USER = st.secrets["DB_USER"]
except Exception:
    POSTGRES_USER = os.getenv("DB_USER", "")

try:
    POSTGRES_PASSWORD = st.secrets["DB_PASSWORD"]
except Exception:
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD", "")

try:
    POSTGRES_PORT = int(st.secrets["DB_PORT"])
except Exception:
    POSTGRES_PORT = int(os.getenv("DB_PORT", 5432))

# ==========================================================
# STREAMLIT
# ==========================================================

PAGE_TITLE = "Enterprise Modern Data Stack Dashboard"

PAGE_LAYOUT = "wide"

CACHE_TIME = 60

# ==========================================================
# DASHBOARD
# ==========================================================

DEFAULT_THEME = "light"

DEFAULT_PAGE_SIZE = 100

# ==========================================================
# API
# ==========================================================

REQUEST_TIMEOUT = 60

MAX_RETRIES = 3

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# DATABASE SCHEMAS
# ==========================================================

STAGING_SCHEMA = "staging"

ANALYTICS_SCHEMA = "analytics"