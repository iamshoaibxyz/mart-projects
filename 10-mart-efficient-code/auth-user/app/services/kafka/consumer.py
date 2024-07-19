from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.schemas.protos import user_pb2 as pb
from app.services.kafka.handle_topics import ( 
    register_new_user, 
    delete_user, 
    verify_reset_password_user, 
    verify_new_user, 
    user_token
)
@asynccontextmanager
async def get_consumer(topic: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers="broker:19092", group_id="mart_group", auto_offset_reset="earliest" )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()

async def kafka_consumer(topic: str):
    async with get_consumer(topic) as consumer:
        async for message in consumer:

            if topic == "user-added":
                user_proto = pb.User()
                user_proto.ParseFromString(message.value)
                await register_new_user(user_proto)

            elif topic == "user-verify-updated":
                user_verify_proto = pb.User()
                user_verify_proto.ParseFromString(message.value) 
                await verify_new_user(user_verify_proto)

            elif topic == "user-token-added":
                user_token_proto = pb.UserToken()
                user_token_proto.ParseFromString(message.value)
                await user_token(user_token_proto)

            elif topic == "user-password-updated":
                user_token_proto = pb.User()
                user_token_proto.ParseFromString(message.value)
                await verify_reset_password_user(user_token_proto)

            elif topic == "user-deleted":
                user_token_proto = pb.User()
                user_token_proto.ParseFromString(message.value)
                await delete_user(user_token_proto)


            else:
                raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found")
            