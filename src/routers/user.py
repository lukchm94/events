from avro.io import BinaryDecoder, DatumReader
from confluent_kafka.error import KafkaError
from fastapi import APIRouter, HTTPException, status

from ..__app_configs import Paths
from ..events.consumer import consumer
from ..events.producer import producer, schema

router = APIRouter(prefix=Paths.user.value, tags=[Paths.user_tag.value])


@router.post(status_code=status.HTTP_201_CREATED)
async def produce_event(user_id: int, user_name: str, user_email: str):
    # Create Avro message
    avro_message = {"id": user_id, "name": user_name, "email": user_email}

    # Produce message to Kafka
    try:
        producer.produce(topic="user_topic", value=avro_message, value_schema=schema)
        producer.flush()
        return {"message": "Event produced successfully"}
    except KafkaError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to produce event: {e.str()}"
        )


@router.get(status_code=status.HTTP_200_OK)
async def consume_event():
    try:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            return {"message": "No events found"}

        if not msg.error():
            # Decode Avro message
            bytes_reader = BinaryDecoder(msg.value())
            decoder = DatumReader(schema)
            user = decoder.read(bytes_reader)

            return {"message": "Event consumed successfully", "user": user}
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            return {"error": str(msg.error())}
    except Exception as e:
        return {"error": str(e)}
