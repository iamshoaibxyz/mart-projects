from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.schemas.protobuf import user_pb2, user_token_pb2, company_pb2, company_token_pb2
from app.services.kafka.handle_topics import verify_reset_password_user, register_new_user, verify_new_user, user_token, register_new_company, verify_new_company, company_token

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

            if topic == "register-new-user-topic":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await register_new_user(user_proto)

            elif topic == "verify-new-user-topic":
                user_verify_proto = user_pb2.User()
                user_verify_proto.ParseFromString(message.value) 
                await verify_new_user(user_verify_proto)

            elif topic == "user-token-topic":
                user_token_proto = user_pb2.UserToken()
                user_token_proto.ParseFromString(message.value)
                await user_token(user_token_proto)

            elif topic == "verify-reset-password-user-topic":
                user_token_proto = user_pb2.User()
                user_token_proto.ParseFromString(message.value)
                await verify_reset_password_user(user_token_proto)

            elif topic == "register-new-company-topic":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await register_new_company(company_proto)

            elif topic == "verify-new-company-topic":
                company_verify_proto = company_pb2.Company()
                company_verify_proto.ParseFromString(message.value) 
                await verify_new_company(company_verify_proto)

            elif topic == "company-token-topic":
                company_token_proto = company_token_pb2.CompanyToken()
                company_token_proto.ParseFromString(message.value) 
                await company_token(company_token_proto)

            else:
                raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found")
            


# async def kafka_consumer(topic:str):
#     consumer = AIOKafkaConsumer(topic, bootstrap_servers="broker:19092", group_id="mart_group" ,auto_offset_reset="earliest")
#     await consumer.start()
#     try:        
#         if topic=="register-new-user-topic111":
#             async for message in consumer:
#                 user_proto = user_pb2.User()
#                 user_proto.ParseFromString(message.value)
#                 await register_new_user(user_proto)
#         else:
#             raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found ",)
#     finally:
#         await consumer.stop()