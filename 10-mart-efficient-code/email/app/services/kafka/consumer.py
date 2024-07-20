from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.schemas.protos import company_pb2, user_pb2, product_pb2, inventory_pb2
from app.services.kafka.handle_topics import (
    email_to_company_transaction_added,
    email_to_company_transaction_subtracted,
    
    email_to_new_company,
    verification_email_to_new_company, 
    email_to_unverified_company, 
    email_to_updated_company ,
    email_to_reset_password_company, 
    email_to_deleted_company,
    email_to_company_password_updated,
    
    email_to_new_user, 
    email_to_unverified_user, 
    email_to_new_verified_user, 
    email_to_reset_password_user,
    email_to_updated_password_user, 
    email_to_deleted_user, 

    email_to_new_product_company, 
    email_to_updated_product_company ,
    # email_to_updated_product_company
    # email_to_new_product_with_transaction ,
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

            if topic == "email-company-added":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_new_company(company_proto)

            elif topic == "email-company-verified-updated":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await verification_email_to_new_company(company_proto)

            elif topic == "email-verification-to-unverified-company":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_unverified_company(company_proto)

            elif topic == "email-company-reset-password":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_reset_password_company(company_proto)

            elif topic == "email-company-info-updated":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_updated_company(company_proto)

            elif topic == "email-company-password-updated":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_company_password_updated(company_proto)

            elif topic == "email-company-deleted":
                company_proto = company_pb2.Company()
                company_proto.ParseFromString(message.value)
                await email_to_deleted_company(company_proto)

            # ======================USER======================

            elif topic == "email-verification-to-unverified-user":
                user_proto = user_pb2.User() 
                user_proto.ParseFromString(message.value)
                await email_to_unverified_user(user_proto)

            elif topic == "email-user-added":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_new_user(user_proto)

            elif topic == "email-user-verified-updated":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_new_verified_user(user_proto)

            elif topic == "email-user-reset-password":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_reset_password_user(user_proto)

            elif topic == "email-user-password-updated":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_updated_password_user(user_proto)

            elif topic == "email-user-deleted":
                user_proto = user_pb2.User()
                user_proto.ParseFromString(message.value)
                await email_to_deleted_user(user_proto)
            

            
            

            elif topic == "email-product-added":
                product_proto = product_pb2.Product()
                product_proto.ParseFromString(message.value)
                await email_to_new_product_company(product_proto)


            elif topic == "email-product-updated":
                product_proto = product_pb2.Product()
                product_proto.ParseFromString(message.value)
                await email_to_updated_product_company(product_proto)

            elif topic == "email-transaction-added":
                transaction_proto = inventory_pb2.InventoryTransaction()
                transaction_proto.ParseFromString(message.value)
                await email_to_company_transaction_added(transaction_proto)


            elif topic == "email-transaction-subtracted":
                transaction_proto = inventory_pb2.InventoryTransaction()
                transaction_proto.ParseFromString(message.value)
                await email_to_company_transaction_subtracted(transaction_proto)



                
            
            # elif topic == "inventory-email-transaction-added":
            #     transaction_proto = customs_pb2.TransactionInfo()
            #     transaction_proto.ParseFromString(message.value)
            #     await email_to_new_product_with_transaction(transaction_proto) 
            

            else:
                raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found")
            