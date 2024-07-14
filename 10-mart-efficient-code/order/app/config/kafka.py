from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session, select, create_engine
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.schemas import order
from app.config.database import DATABASE_URL

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def kafka_consumer(topic:str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers="broker:19092", group_id="mart_group" ,auto_offset_reset="earliest")
    await consumer.start()
    try:  
        
        if topic=="something-topic":
            async for message in consumer:
                pass
        else:
            raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found ",)

    finally:
        await consumer.stop()

