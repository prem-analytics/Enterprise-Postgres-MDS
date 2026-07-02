{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        o.order_id,
        o.customer_id,
        c.customer_country,
        o.order_placed_at,
        o.order_status,
        o.order_total_usd,
        o.payment_method,
        c.account_created_at
    from orders o
    left join customers c on o.customer_id = c.customer_id
)

select * from final