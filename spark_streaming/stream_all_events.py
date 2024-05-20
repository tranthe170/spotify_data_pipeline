# Run the script using the following command
# spark-submit \
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
# stream_all_events.py
import os

from schema import schema
from streaming_functions import *
from schema import EVENTS_SCHEMA, PROCESSED_SCHEMA

# Kafka Topics
KAFKA_EVENTS_TOPIC = 'spotify'
KAFKA_PORT = "9092"

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')
GCP_GCS_BUCKET = os.getenv("GCP_GCS_BUCKET", 'spotify-stream-bucket-17052024')
GCS_STORAGE_PATH = f'gs://{GCP_GCS_BUCKET}'

# initialize a spark session
spark = create_or_get_spark_session('Eventsim Stream')
spark.streams.resetTerminated()
# user stream
kafka_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, KAFKA_EVENTS_TOPIC)
kafka_events = process_stream(
    kafka_events, EVENTS_SCHEMA, KAFKA_EVENTS_TOPIC)

# write a file to storage every 2 minutes in parquet format
kafka_writer = create_file_write_stream(kafka_events,
                                                f"{GCS_STORAGE_PATH}/{KAFKA_EVENTS_TOPIC}",
                                                f"{GCS_STORAGE_PATH}/checkpoint/{KAFKA_EVENTS_TOPIC}"
                                                )

kafka_writer.start()

spark.streams.awaitAnyTermination()