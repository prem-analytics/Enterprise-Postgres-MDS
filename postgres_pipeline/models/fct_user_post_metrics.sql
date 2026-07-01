{{ config(materialized='table') }}

with staged_posts as (
    select * from {{ ref('stg_posts') }}
)

select
    user_id,
    count(post_id) as total_posts_created,
    round(avg(body_character_count), 2) as average_post_length_characters,
    case 
        when count(post_id) >= 15 then 'Power User'
        when count(post_id) >= 5 then 'Active Contributor'
        else 'Standard Contributor'
    end as user_engagement_tier
from staged_posts
group by user_id