INSERT {{ BIGQUERY_DATASET }}.{{ SPOTIFY_EVENTS_TABLE }}
SELECT
    COALESCE(first_name, 'NA') AS firstName,
    COALESCE(last_name, 'NA') AS lastName,
    COALESCE(gender, 'NA') AS gender,
    COALESCE(city, 'NA') AS city,
    COALESCE(state, 'NA') AS state,
    COALESCE(country, 'NA') AS country,
    COALESCE(latitude, 0.0) AS latitude,
    COALESCE(longitude, 0.0) AS longitude,
    COALESCE(listen_timestamp, 0) AS listenTimestamp,
    COALESCE(song_id, 'NA') AS songId,
    COALESCE(artist_name, 'NA') AS artistName,
    COALESCE(artist_id, 'NA') AS artistId,
    COALESCE(song_title, 'NA') AS songTitle,
    COALESCE(album_name, 'NA') AS albumName,
    COALESCE(release_date, 'NA') AS releaseDate,
    COALESCE(duration_ms, 0) AS durationMs,
    COALESCE(danceability, 0.0) AS danceability,
    COALESCE(energy, 0.0) AS energy,
    COALESCE(key, 0) AS key,
    COALESCE(loudness, 0.0) AS loudness,
    COALESCE(mode, 0) AS mode,
    COALESCE(speechiness, 0.0) AS speechiness,
    COALESCE(acousticness, 0.0) AS acousticness,
    COALESCE(instrumentalness, 0.0) AS instrumentalness,
    COALESCE(liveness, 0.0) AS liveness,
    COALESCE(valence, 0.0) AS valence,
    COALESCE(tempo, 0.0) AS tempo,
    COALESCE(year, 0) AS year,
    COALESCE(month, 0) AS month,
    COALESCE(day, 0) AS day,
    COALESCE(hour, 0) AS hour
    COALESCE(duration_minutes, 0.0) AS durationMinutes,
    COALESCE(full_name, 'NA') AS fullName,
FROM {{ BIGQUERY_DATASET }}.{{ SPOTIFY_EVENTS_TABLE}}_{{ logical_date.strftime("%m%d%H") }}