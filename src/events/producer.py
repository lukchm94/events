from io import BytesIO

from avro.io import BinaryEncoder, DatumWriter
from avro.schema import Parse
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

# Load Avro schema
schema = Parse(open("src/events/schemas/user.avsc", "rb").read())


# Serializer function
def avro_serializer(data, ctx):
    bytes_io = BytesIO()
    writer = DatumWriter(schema)
    encoder = BinaryEncoder(bytes_io)
    writer.write(data, encoder)
    return bytes_io.getvalue()


# Configure the schema registry URL directly in the avro_serializer function
avro_serializer_conf = {"schema.registry.url": "http://localhost:8081"}

producer_conf = {
    "bootstrap.servers": "localhost:9092",
    "key.serializer": StringSerializer("utf_8"),
    # Pass the Avro serializer function directly to value.serializer
    "value.serializer": avro_serializer,
    "value.serializer.schema.registry.url": "http://localhost:8081",  # Specify schema registry URL here
}

producer = SerializingProducer(producer_conf)
