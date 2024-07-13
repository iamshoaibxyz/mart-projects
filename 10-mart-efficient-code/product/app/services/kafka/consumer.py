from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.schemas.protos import all_proto_pb2, customs_pb2
from app.services.kafka.handle_topics import add_new_product, add_new_product_with_inventory, update_product

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
         
            if topic == "product-product-product-added":
                product_proto = all_proto_pb2.Product()
                product_proto.ParseFromString(message.value)
                await add_new_product(product_proto)
         
            elif topic == "product_product_product_updated":
                product_proto = all_proto_pb2.Product()
                product_proto.ParseFromString(message.value)
                await update_product(product_proto)
         
            elif topic == "product-product-product-and-inventory-added":
                product_proto = customs_pb2.ProductWithInventory()
                product_proto.ParseFromString(message.value)
                await add_new_product_with_inventory(product_proto)


            # elif topic == "product-product-product-and-inventory-added":
            #     product_proto = all_proto_pb2.ProductStockModel()
            #     product_proto.ParseFromString(message.value)
            #     await add_new_product_with_inventory(product_proto)

            # elif topic == "verify-new-company-topic":
            #     company_verify_proto = all_proto_pb2.Company()
            #     company_verify_proto.ParseFromString(message.value) 
            #     await verify_new_company(company_verify_proto)

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