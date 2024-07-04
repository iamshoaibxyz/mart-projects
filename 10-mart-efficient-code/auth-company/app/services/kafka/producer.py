from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer

@asynccontextmanager
async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
