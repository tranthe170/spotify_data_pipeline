import time
import json
import pandas as pd
from confluent_kafka import Producer

class KafkaStreamer:
    def __init__(self, broker_address: str) -> None:
        self.producer = Producer({'bootstrap.servers': broker_address})

    def produce_dataframe(self, topic: str, dataframe: pd.DataFrame) -> bool:
        for row in dataframe.itertuples(index=False):
            print(row)
            key_bytes = str(time.time()).encode("utf-8")
            value_bytes = json.dumps(row._asdict()).encode("utf-8")

            self.producer.produce(topic, value=value_bytes, key=key_bytes)
            # add delay
            time.sleep(0.5)

        self.producer.flush()