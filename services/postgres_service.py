import pandas as pd
import psycopg2

from config.config import (
    POSTGRES_HOST,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    STAGING_SCHEMA,
    ANALYTICS_SCHEMA,
)

# =======================================================
# PostgreSQL Connection
# =======================================================

def get_connection():

    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )


# =======================================================
# Execute Query
# =======================================================

def execute_query(query):

    conn = get_connection()

    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    return df


# =======================================================
# PostgreSQL Version
# =======================================================

def get_version():

    return execute_query(
        "SELECT version();"
    )


# =======================================================
# Database Size
# =======================================================

def get_database_size():

    query = """
    SELECT
        pg_size_pretty(
            pg_database_size(current_database())
        ) AS database_size;
    """

    return execute_query(query)


# =======================================================
# Active Connections
# =======================================================

def get_active_connections():

    query = """
    SELECT COUNT(*) AS active_connections
    FROM pg_stat_activity;
    """

    return execute_query(query)


# =======================================================
# Schema Count
# =======================================================

def get_schema_count():

    query = """
    SELECT COUNT(*) AS schemas
    FROM information_schema.schemata;
    """

    return execute_query(query)


# =======================================================
# List Schemas
# =======================================================

def get_schemas():

    query = f"""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name IN (
        '{STAGING_SCHEMA}',
        '{ANALYTICS_SCHEMA}'
    )
    ORDER BY schema_name;
    """

    return execute_query(query)


# =======================================================
# List Tables
# =======================================================

def get_tables():

    query = f"""
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_type='BASE TABLE'
      AND table_schema IN (
        '{STAGING_SCHEMA}',
        '{ANALYTICS_SCHEMA}'
      )
    ORDER BY table_schema,
             table_name;
    """

    return execute_query(query)


# =======================================================
# View Count
# =======================================================

def get_view_count():

    query = f"""
    SELECT COUNT(*) AS views
    FROM information_schema.views
    WHERE table_schema IN (
        '{STAGING_SCHEMA}',
        '{ANALYTICS_SCHEMA}'
    );
    """

    return execute_query(query)


# =======================================================
# Database Statistics
# =======================================================

def get_database_statistics():

    query = f"""
    SELECT

        (
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema IN (
                '{STAGING_SCHEMA}',
                '{ANALYTICS_SCHEMA}'
            )
        ) AS tables,

        (
            SELECT COUNT(*)
            FROM information_schema.views
            WHERE table_schema IN (
                '{STAGING_SCHEMA}',
                '{ANALYTICS_SCHEMA}'
            )
        ) AS views,

        (
            SELECT COUNT(*)
            FROM pg_indexes
            WHERE schemaname IN (
                '{STAGING_SCHEMA}',
                '{ANALYTICS_SCHEMA}'
            )
        ) AS indexes;
    """

    return execute_query(query)


# =======================================================
# Table Row Count
# =======================================================

def get_table_count(schema, table):

    query = f"""
    SELECT COUNT(*) AS total
    FROM {schema}.{table};
    """

    return int(
        execute_query(query)["total"][0]
    )


# =======================================================
# Preview Table
# =======================================================

def preview_table(schema, table, limit=20):

    query = f"""
    SELECT *
    FROM {schema}.{table}
    LIMIT {limit};
    """

    return execute_query(query)


# =======================================================
# Column Metadata
# =======================================================

def get_columns(schema, table):

    query = f"""
    SELECT

        column_name,
        data_type,
        is_nullable

    FROM information_schema.columns

    WHERE table_schema='{schema}'
      AND table_name='{table}'

    ORDER BY ordinal_position;
    """

    return execute_query(query)


# =======================================================
# Database Objects
# =======================================================

def get_database_objects():

    query = f"""
    SELECT

        table_schema,
        table_name,
        table_type

    FROM information_schema.tables

    WHERE table_schema IN (
        '{STAGING_SCHEMA}',
        '{ANALYTICS_SCHEMA}'
    )

    ORDER BY
        table_schema,
        table_name;
    """

    return execute_query(query)