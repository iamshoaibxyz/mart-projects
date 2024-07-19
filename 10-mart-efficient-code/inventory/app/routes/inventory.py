from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import SQLModel, select, Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
from aiokafka import AIOKafkaProducer
from typing import Annotated
from uuid import UUID

from app.schemas.inventory import InventoryAddReq, InventoryTransactionSchema, StockLevelSchema
from app.models.inventory import InventoryTransaction, StockLevel
from app.schemas.protos import inventory_pb2, customs_pb2
from app.config.database import get_session
from app.services.kafka.producer import get_producer
from app.utils.fetcher import fetch_product_detail_by_id, auth_checker

oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/company/company-login")

router = APIRouter(prefix="/inventory", tags=["Inventory"], responses={404:{"description": "Not found"}})

@router.post("/add-inventory")
async def add_inventory(product_data: InventoryAddReq, token: Annotated[dict, Depends(oauth2_company_scheme)]):
    company = await auth_checker(token=token)
    product = await fetch_product_detail_by_id(product_data.product_id, company.get("id"))
    # return {"company": company, "product": product}
    inventory_proto = customs_pb2.InventoryInfo(company_id=str(company.get("id")), product_id=str(product.get("id")), stock=int(product_data.quantity) )
    async with get_producer() as producer:
        await producer.send_and_wait("inventory-added", inventory_proto.SerializeToString())
    return {"message": "Stock added successfully"} 

@router.post("/subtract-inventory")
async def subtract_inventory(product_data: InventoryAddReq, session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_company_scheme)]):
    company = await auth_checker(token=token)
    product = await fetch_product_detail_by_id(product_data.product_id)
    stock = session.exec(select(StockLevel).where(StockLevel.product_id==UUID(product_data.product_id))).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="stock not found")
    if stock.current_stock < product_data.quantity:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Insufficient stock, we have just '{stock.current_stock}' item of {product.get("name")} by {company.get("name")} company/shop")
    inventory_proto = customs_pb2.InventoryInfo(company_id=str(company.get("id")), product_id=str(product.get("id")), stock=int(product_data.quantity) )
    async with get_producer() as producer:
        await producer.send_and_wait("inventory-subtracted", inventory_proto.SerializeToString())
    return {"message": "Stock subtracted successfully"} 

@router.get("/get-all-stocks", response_model=list[StockLevelSchema])
async def all_stocks(session: Annotated[Session, Depends(get_session)]):
    stock = session.exec(select(StockLevel)).all()
    return stock

@router.get("/get-all-inventory-transactions", response_model=list[InventoryTransactionSchema])
async def all_transactions(session: Annotated[Session, Depends(get_session)]):
    inventory = session.exec(select(InventoryTransaction)).all()
    return inventory

@router.get("/get-all-transactions-by-product-id/{product_id}", response_model=list[InventoryTransactionSchema])
async def transactions_by_product_id(product_id: str ,session: Annotated[Session, Depends(get_session)]):
    transactions = session.exec(select(InventoryTransaction).where(InventoryTransaction.product_id==UUID(product_id))).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product's transactions not found")
    return transactions
 

@router.get("/get-transaction-by-id/{transaction_id}", response_model=InventoryTransactionSchema)
async def transaction_by__id(transaction_id: str ,session: Annotated[Session, Depends(get_session)]):
    transactions = session.exec(select(InventoryTransaction).where(InventoryTransaction.id==UUID(transaction_id))).first()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"transactions not found")
    return transactions
 
@router.get("/get-stock-by-product-id/{product_id}", response_model=StockLevelSchema)
async def stocks_by_product_id(product_id: str ,session: Annotated[Session, Depends(get_session)]):
    stock = session.exec(select(StockLevel).where(StockLevel.product_id==UUID(product_id))).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product's stock not found")
    return stock

@router.get("/get-stock-by-id/{stock_id}", response_model=StockLevelSchema)
async def stocks_by_id(stock_id: str ,session: Annotated[Session, Depends(get_session)]):
    stock = session.exec(select(StockLevel).where(StockLevel.id==UUID(stock_id))).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"stock not found")
    return stock
















    # return {"product_data": product_data, "product_exist": product_exist, "inventory": inventory} 

    # new_product = productModel(first_name=product.first_name, last_name=product.last_name, password=product.password, email=product.email)
    # product_protobuf = mart_pb2.Product(id=str(ready_product.id), name= ready_product.name, price=ready_product.price, category= ready_product.category, quantity= ready_product.quantity)
    # serialized_product = product_protobuf.SerializeToString()
    # protobuf_product = product_pb2.product()
    # producer.send_and_wait("")