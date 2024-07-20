from contextlib import asynccontextmanager
from sqlmodel import Session, create_engine
from uuid import UUID
import logging
import json

from app.config.settings import PRODUCT_DATABASE_URL
from app.services.kafka.producer import get_producer
from app.schemas.protos import customs_pb2
from app.models.product import ProductModel
from app.utils.proto_conversion import proto_to_product 

logger = logging.getLogger(__name__)
connection_str = str(PRODUCT_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def add_new_product(product_proto):
    new_product = proto_to_product(product_proto)
    async with get_session() as session:
        session.add(new_product)
        session.commit() 
        session.refresh(new_product)
    async with get_producer() as producer:
        await producer.send_and_wait("email-product-added", product_proto.SerializeToString())

async def update_product(product_proto):
    updated_product = proto_to_product(product_proto)
    async with get_session() as session:
        product = session.get(ProductModel, updated_product.id)
        product.sqlmodel_update(updated_product)
        session.add(product)
        session.commit() 
        session.refresh(product)
    async with get_producer() as producer:
        await producer.send_and_wait("email-product-updated", product_proto.SerializeToString())

async def add_new_product_with_inventory(product_proto):
    product = ProductModel(name=product_proto.name, description=product_proto.description, price=float(product_proto.price), category=product_proto.category, company_id=UUID(product_proto.company_id))
    product_info = product.model_copy()
    async with get_session() as session:
        session.add(product) 
        session.commit()  
        session.refresh(product)

    async with get_producer() as producer:
        await producer.send_and_wait("hello", b"product added")
        proto_inventory_info = customs_pb2.InventoryInfo(company_id=str(product_info.company_id), product_id=str(product_info.id), stock=int(product_proto.stock))
        await producer.send_and_wait("inventory-new-stock-added", proto_inventory_info.SerializeToString())
        







# async def add_new_product_with_inventory(product_proto):
#     product = proto_to_productmodel(product_proto)    
#     async with get_session() as session:
#         company = await session.get(CompanyModel, product.company_id)
#         if company:
#             company.products.append(product)            
#             stock = product.stock.model_copy()            
#             transaction = InventoryTransaction(
#                 stock_id=stock.id,
#                 product_id=product.id,
#                 quantity=stock.current_stock,
#                 product=product,
#                 operation=Operation.ADD )            
#             stock.transactions.append(transaction)
#             stock.product = product
#             transaction.stock = stock
#             session.add(company)
#             session.add(stock)
#             session.add(transaction)
#             await session.commit()
#             await session.refresh(company)
#             await session.refresh(stock)
#             await session.refresh(transaction)
#         else:
#             logger.error(f"Company with ID {product.company_id} not found.")
#             return
    
#     try:
#         async with get_producer() as producer:
#             transaction_proto = inventory_transaction_to_proto(transaction)
#             await producer.send_and_wait("product-inventory-stock-added", transaction_proto.SerializeToString())
#             logger.info(f"Produced message to 'product-inventory-stock-added': {transaction_proto}")
#     # except KafkaError as e:
#     #     logger.error(f"Failed to produce message: {e}")
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
 
# async def add_new_product_with_inventory(product_proto):
    # product = proto_to_product_stock(product_proto)
    # new_product = ProductModel(name=product.name, description=product.description, price=product.price, category=product.category, company_id=product.company_id)
    # stock = StockLevel(product_id=new_product.id, current_stock=int(product.stock), product=new_product)
    # transaction = InventoryTransaction(stock_id=stock.id, product_id=new_product.id, quantity=product.stock, stock=stock, product=new_product )
    
    # stock.transactions.append(transaction)
    # new_product.transactions.append(transaction)

    # async with get_session() as session:
    #     company = session.get(CompanyModel, new_product.company_id)
    #     company.products.append(new_product)
    #     session.add(transaction)
    #     session.add(new_product)
    #     session.commit() 
    #     session.refresh(company)

    # async with get_producer() as producer:
    #     await producer.send_and_wait("helloworld", b"Inventory {qwertyupoi}")
        # stock_proto = stocklevel_to_proto(stock)
        # await producer.send_and_wait("product-inventory-stock-added", stock_proto.SerializeToString())
    
    # stock.product = new_product
    # transactions = InventoryTransaction(operation=Operation.ADD, stock=stock, stock_id=UUID(stock.id), quantity=int(stock.current_stock), product_id=UUID(new_product.id), product=new_product)
    # stock.transactions.append(transactions)
    # async with get_producer() as producer:
    #     await producer.send_and_wait("helloworld", b"Inventory {}")
        # stock_proto = stocklevel_to_proto(stock)
        # await producer.send_and_wait("product-inventory-stock-added", stock_proto.SerializeToString())



# async def verify_new_company(company_proto):
#     company_model = proto_to_company(company_proto)
#     async with get_session() as session:
#         company = session.get(CompanyModel, company_model.id)
#         company.is_verified = True
#         company.verified_at = datetime.now(timezone.utc)
#         company.updated_at = datetime.now(timezone.utc)
#         session.add(company)
#         session.commit()
#         session.refresh(company)
#     # send to kafka and then email-service will be recived
#     async with get_producer() as producer:
#         proto_company = company_to_proto(company)
#         await producer.send_and_wait("email-to-new-verify-company-topic", proto_company.SerializeToString())
