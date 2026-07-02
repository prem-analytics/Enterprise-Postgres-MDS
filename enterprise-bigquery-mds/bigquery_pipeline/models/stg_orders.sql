{{ config(materialized='view') }}

with source as (
    select * from {{ source('bq_staging', 'raw_orders') }}
),

renamed as (
    select
        cast(order_id as string) as order_id,
        cast(customer_id as string) as customer_id,
        timestamp(order_date) as order_placed_at,
        cast(status as string) as order_status,
        cast(order_total as numeric) as order_total_usd,
        cast(payment_method as string) as payment_method
    from source
)

select * from renamed