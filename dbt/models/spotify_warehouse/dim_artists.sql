{% from 'dbt_utils' import generate_surrogate_key %}
{{
  config(
    materialized='incremental',
    unique_key='artistKey',
    incremental_strategy = 'merge',
    merge_update_columns = ['artistName', 'artistId'],
    transient=false
  )
}}
SELECT distinct artist_id as artistId, artist_name as artistName,
        {{ generate_surrogate_key(['artistId']) }} AS artistKey
    from {{source('spotify_staging','spotify')}};