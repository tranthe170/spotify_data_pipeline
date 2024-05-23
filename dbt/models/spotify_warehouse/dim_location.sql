{% from 'dbt_utils' import generate_surrogate_key %}
{{
  config(
    materialized='incremental',
    unique_key='locationKey',
    incremental_strategy = 'merge',
    transient=false
  )
}}

with final as (
    SELECT distinct
    city,
    state,
    country,
    latitude,
    longitude
    FROM  {{source('spotify_staging','spotify')}}
)

SELECT {{ generate_surrogate_key(['latitude', 'longitude', 'city', 'state', 'country']) }} as locationKey,
*
FROM final where exists (select 1 from final)




