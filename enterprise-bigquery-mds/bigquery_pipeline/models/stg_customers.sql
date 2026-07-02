{{ config(materialized='view') }}

with source as (
    select * from {{ source('bq_staging', 'raw_customers') }}
),

renamed as (
    select
        cast(customer_id as string) as customer_id,
        cast(first_name as string) as first_name,
        cast(country as string) as customer_country,
        timestamp(created_at) as account_created_at
    from source
)

select * from renamed