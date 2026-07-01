{{ config(materialized='view') }}

with source_data as (
    select * from {{ source('raw_source', 'stg_raw_posts') }}
)

select
    id as post_id,
    user_id,
    trim(title) as post_title,
    trim(body) as post_body,
    length(body) as body_character_count
from source_data