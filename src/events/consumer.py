from avro.io import BinaryDecoder, DatumReader
from avro.schema import Parse
from confluent_kafka import Consumer
from confluent_kafka.error import KafkaError

schema = Parse(open("src/events/schemas/user.avsc", "rb").read())

consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}

consumer: Consumer = Consumer(consumer_conf)
