from io import BytesIO

from avro.io import BinaryEncoder, DatumWriter
from avro.schema import Parse
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

# Producer configuration
producer_conf = {
    "bootstrap.servers": "localhost:9092",  # Kafka broker address
    "key.serializer": StringSerializer("utf_8"),
    # You might not need to specify the value serializer here if you're using a custom serializer as you have done in your original code.
    # "value.serializer": avro_serializer,  # Specify your Avro serializer function here if needed
}

# Create a Kafka producer
producer = SerializingProducer(producer_conf)

# Load Avro schema
schema = Parse(open("src/events/schemas/user.avsc", "rb").read())


def avro_serializer(data, ctx):
    bytes_io = BytesIO()
    writer = DatumWriter(schema)
    encoder = BinaryEncoder(bytes_io)
    writer.write(data, encoder)
    return bytes_io.getvalue()
