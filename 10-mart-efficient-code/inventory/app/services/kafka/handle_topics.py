from contextlib import asynccontextmanager
import json
from sqlmodel import Session, create_engine, select
from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from app.utils.proto_conversion import  inventory_transaction_to_proto
from app.config.settings import INVENTORY_DATABASE_URL
from app.services.kafka.producer import get_producer
from app.models.inventory import InventoryTransaction, StockLevel
from app.schemas.protos import customs_pb2

connection_str = str(INVENTORY_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def add_inventory_stock(stock_proto):
    try:
        transaction_info: Any
        async with get_session() as session:
            stock = session.exec(select(StockLevel).where(StockLevel.product_id == UUID(stock_proto.product_id))).first()
            if not stock:
                stock = StockLevel(product_id=UUID(stock_proto.product_id), current_stock=0)
                session.add(stock)
            transaction  = InventoryTransaction(stock_id=stock.id, product_id=stock.product_id, quantity=int(stock_proto.stock), operation="add" )
            session.add(transaction)
            
            stock.current_stock += transaction.quantity

            session.commit() 
            session.refresh(stock)
            session.refresh(transaction)
            transaction_info = transaction.model_copy()

        async with get_producer() as producer:
            transaction_proto = inventory_transaction_to_proto(transaction_info)
            await producer.send_and_wait("email-transaction-added", transaction_proto.SerializeToString())
    except Exception as e:
        async with get_producer() as producer:
            string_error = f"{str(e)}, something went wrong during initiolizing stock and transaction"
            error = json.dumps(string_error).encode("utf-8")
            await producer.send_and_wait("error", error.SerializeToString())



async def subtract_inventory_stock(stock_proto):
    try:
        transaction_info: Any
        async with get_session() as session:
            stock = session.exec(select(StockLevel).where(StockLevel.product_id == UUID(stock_proto.product_id))).first()
            transaction  = InventoryTransaction(stock_id=stock.id, product_id=stock.product_id, quantity=int(stock_proto.stock), operation="subtract" )
            session.add(transaction)
            
            stock.current_stock -= transaction.quantity

            session.commit() 
            session.refresh(stock)
            session.refresh(transaction)
            transaction_info = transaction.model_copy()

        async with get_producer() as producer:
            transaction_proto = inventory_transaction_to_proto(transaction_info)
            await producer.send_and_wait("email-transaction-subtracted", transaction_proto.SerializeToString())
    except Exception as e:
        async with get_producer() as producer:
            string_error = f"{str(e)}, something went wrong during subtracting stock"
            error = json.dumps(string_error).encode("utf-8")
            await producer.send_and_wait("error", error.SerializeToString())


# async def add_new_inventory_stock(stock_proto):
#     try:
#         transaction_info: Any
#         async with get_session() as session:
#             stock = session.exec(select(StockLevel).where(StockLevel.product_id == UUID(stock_proto.product_id))).first()
#             if not stock:
#                 stock = StockLevel(product_id=UUID(stock_proto.product_id), current_stock=0)
#                 session.add(stock)
#             transaction  = InventoryTransaction(stock_id=stock.id, product_id=stock.product_id, quantity=int(stock_proto.stock), operation="add" )
#             session.add(transaction)
            
#             stock.current_stock += transaction.quantity

#             session.commit() 
#             session.refresh(stock)
#             session.refresh(transaction)
#             transaction_info = transaction.model_copy()

#         async with get_producer() as producer:
#             transaction_proto = inventory_transaction_to_proto(transaction_info)
#             await producer.send_and_wait("email-transaction-added", transaction_proto.SerializeToString())
#     except Exception as e:
#         async with get_producer() as producer:
#             string_error = f"{str(e)}, something went wrong during initiolizing stock and transaction"
#             error = json.dumps(string_error).encode("utf-8")
#             await producer.send_and_wait("error", error.SerializeToString())


