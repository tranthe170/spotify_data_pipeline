# Run the script using the following command
# spark-submit \
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
# stream_all_events.py
import os

from schema import schema
from streaming_functions import *

# Kafka Topics
USERS_TOPIC = "users"
PRODUCTS_TOPIC = "products"
CLICK_EVENTS_TOPIC = "click_events"
CHECKOUT_EVENTS_TOPIC = "checkout_events"
KAFKA_PORT = "9092"

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')
GCP_GCS_BUCKET = os.getenv("GCP_GCS_BUCKET", 'spotify-stream-bucket-17052024')
GCS_STORAGE_PATH = f'gs://{GCP_GCS_BUCKET}'

# initialize a spark session
spark = create_or_get_spark_session('Eventsim Stream')
spark.streams.resetTerminated()
# user stream
user_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, USERS_TOPIC)
user_events = process_stream(
    user_events, schema[USERS_TOPIC], USERS_TOPIC)

# products stream
products_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, PRODUCTS_TOPIC)
products_events = process_stream(
    products_events, schema[PRODUCTS_TOPIC], PRODUCTS_TOPIC)

# clicks events stream
clicks_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, CLICK_EVENTS_TOPIC)
clicks_events = process_stream(
    clicks_events, schema[CLICK_EVENTS_TOPIC], CLICK_EVENTS_TOPIC)
# checkout events stream
checkout_events = create_kafka_read_stream(
    spark, KAFKA_ADDRESS, KAFKA_PORT, CHECKOUT_EVENTS_TOPIC)
checkout_events = process_stream(
    checkout_events, schema[CHECKOUT_EVENTS_TOPIC], CHECKOUT_EVENTS_TOPIC)

# write a file to storage every 2 minutes in parquet format
user_writer = create_file_write_stream(user_events,
                                                f"{GCS_STORAGE_PATH}/{USERS_TOPIC}",
                                                f"{GCS_STORAGE_PATH}/checkpoint/{USERS_TOPIC}"
                                                )
products_writer = create_file_write_stream(products_events,
                                             f"{GCS_STORAGE_PATH}/{PRODUCTS_TOPIC}",
                                                f"{GCS_STORAGE_PATH}/checkpoint/{PRODUCTS_TOPIC}"
                                                )
clicks_writer = create_file_write_stream(clicks_events,
                                                f"{GCS_STORAGE_PATH}/{CLICK_EVENTS_TOPIC}",
                                                    f"{GCS_STORAGE_PATH}/checkpoint/{CLICK_EVENTS_TOPIC}"
                                                    )
checkout_writer = create_file_write_stream(checkout_events,
                                                f"{GCS_STORAGE_PATH}/{CHECKOUT_EVENTS_TOPIC}",
                                                    f"{GCS_STORAGE_PATH}/checkpoint/{CHECKOUT_EVENTS_TOPIC}"
                                                    )

user_writer.start()
products_writer.start()
clicks_writer.start()
checkout_writer.start()

spark.streams.awaitAnyTermination()