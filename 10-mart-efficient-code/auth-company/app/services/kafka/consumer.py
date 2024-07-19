from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException

from app.schemas.protos import company_pb2
from app.services.kafka.handle_topics import (
    delete_company, 
    update_company, 
    verify_reset_password_company, 
    register_new_company, 
    verify_new_company, 
    company_token
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
         
            if topic == "company-added":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await register_new_company(company_proto)

            elif topic == "company-verify-updated":
                company_verify_proto = company_pb2.Company()
                company_verify_proto.ParseFromString(message.value) 
                await verify_new_company(company_verify_proto)

            elif topic == "company-token-added":
                company_token_proto = company_pb2.CompanyToken()
                company_token_proto.ParseFromString(message.value) 
                await company_token(company_token_proto)

            elif topic == "company-password-updated":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value) 
                await verify_reset_password_company(company_proto)

            elif topic == "company-updated":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value) 
                await update_company(company_proto)

            elif topic == "company-deleted":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value) 
                await delete_company(company_proto)

            
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