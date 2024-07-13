from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
# from app.services.database.session import get_session
from sqlmodel import Session, create_engine, select
from app.utils.proto_utils import  proto_to_productmodel, inventory_transaction_to_proto
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.all_models import CompanyModel, ProductModel, InventoryTransaction, StockLevel, Operation
from uuid import UUID
from app.schemas.protos import customs_pb2
from typing import Any

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def add_new_inventory_stock(stock_proto):
    # transaction_info: Any
    async with get_session() as session:
        stock = StockLevel(product_id=UUID(stock_proto.product_id), current_stock=int(stock_proto.stock))
        transaction  = InventoryTransaction(stock_id=stock.id, product_id=stock.product_id, quantity=int(stock_proto.stock), operation=Operation.ADD )
        product = session.get(ProductModel, stock.product_id)
        
        transaction.product = product
        transaction.stock = stock
        stock.product = product
        stock.transactions.append(transaction)
        session.add(stock)
        session.add(transaction)

        product.transactions.append(transaction)

        session.commit() 
        session.refresh(product)
        session.refresh(stock)
        session.refresh(transaction)
        # transaction_info = transaction.model_copy() 

    async with get_producer() as producer:
        await producer.send_and_wait("hello", b" inventory transaction ")
        transaction_proto = customs_pb2.TransactionInfo(transaction_id=str(transaction.id))
        await producer.send_and_wait("inventory-email-transaction-added", transaction_proto.SerializeToString())
        # await producer.send_and_wait("hello", transaction_info.model_dump_json().encode("utf-8") )
