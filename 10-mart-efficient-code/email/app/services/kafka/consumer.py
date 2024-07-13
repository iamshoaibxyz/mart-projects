from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.protobuf import company_pb2
from app.schemas.protos import all_proto_pb2, customs_pb2
from app.services.kafka.handle_topics import (
    email_to_new_product_with_transaction ,
    email_to_new_product_company, 
    email_to_reset_password_company, 
    verify_email_to_new_company, 
    email_to_unverified_company, 
    email_to_new_company ,
    email_verify_reset_user_password, 
    email_to_new_user, 
    email_to_new_verified_user, 
    email_to_unverified_user, 
    email_to_reset_password_user,
    email_to_updated_product_company
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

            if topic == "email-to-unverified-user-topic":
                user_proto = all_proto_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_unverified_user(user_proto)

            if topic == "email-to-new-user-topic":
                user_proto = all_proto_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_new_user(user_proto)

            if topic == "email-to-new-verified-user-topic":
                user_proto = all_proto_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_new_verified_user(user_proto)

            elif topic == "email-to-reset-password-user-topic":
                user_proto = all_proto_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_reset_password_user(user_proto)

            elif topic == "email-verify-reset-password-user-topic":
                user_proto = all_proto_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_verify_reset_user_password(user_proto)




            elif topic == "email-to-new-company-topic":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_new_company(company_proto)

            elif topic == "email-to-new-verify-company-topic":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await verify_email_to_new_company(company_proto)

            elif topic == "email-to-unverified-company-topic":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_unverified_company(company_proto)


            elif topic == "email-to-reset-password-company-topic":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_reset_password_company(company_proto)
            

            elif topic == "product-email-product-added":
                product_proto = all_proto_pb2.Product()
                product_proto.ParseFromString(message.value)
                await email_to_new_product_company(product_proto) 

            elif topic == "product-email-product-updated":
                product_proto = all_proto_pb2.Product()
                product_proto.ParseFromString(message.value)
                await email_to_updated_product_company(product_proto)
                
            
            elif topic == "inventory-email-transaction-added":
                transaction_proto = customs_pb2.TransactionInfo()
                transaction_proto.ParseFromString(message.value)
                await email_to_new_product_with_transaction(transaction_proto) 
            

            else:
                raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found")
            