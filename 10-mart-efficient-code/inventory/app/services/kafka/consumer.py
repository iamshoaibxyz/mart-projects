from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import HTTPException
from aiokafka import AIOKafkaConsumer
from app.schemas.protos import inventory_pb2, customs_pb2
from app.services.kafka.handle_topics import  add_new_inventory_stock, subtract_inventory_stock

@asynccontextmanager
async def get_consumer(topic: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers="broker:19092", group_id="mart_group", auto_offset_reset="earliest" )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()
 
# InventoryTransaction, StockLevel

async def kafka_consumer(topic: str):
    async with get_consumer(topic) as consumer:
        async for message in consumer:
         
            if topic == "inventory-added":
                inventory_proto = customs_pb2.InventoryInfo()
                inventory_proto.ParseFromString(message.value)
                await add_new_inventory_stock(inventory_proto)
         
         
            elif topic == "inventory-subtracted":
                inventory_proto = customs_pb2.InventoryInfo()
                inventory_proto.ParseFromString(message.value)
                await subtract_inventory_stock(inventory_proto)
         
            # elif topic == "product-product-and-inventory-added":
            #     product_proto = all_proto_pb2.Product()
            #     product_proto.ParseFromString(message.value)
            #     await add_new_product_with_inventory(product_proto)


            else:
                raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found")
