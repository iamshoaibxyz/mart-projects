from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import SQLModel, select, Session
from app.schemas.inventory import InventoryAddReq, InventorySubtractReq, InventoryTransactionSchema, StockLevelSchema, ProductModelSchema
from app.models.all_models import InventoryTransaction, StockLevel, ProductModel, Operation
from app.config.kafka import get_producer
from app.config.database import get_session
from aiokafka import AIOKafkaProducer
from typing import Annotated
from uuid import UUID
from datetime import datetime, timezone

from app.schemas.protos import all_proto_pb2

router = APIRouter(prefix="/inventory", tags=["Inventory"], responses={404:{"description": "Not found"}})

@router.post("/add-inventory")
async def add_inventory(product_data: InventoryAddReq, session: Annotated[Session, Depends(get_session)]):
    product_exist = session.exec(select(ProductModel).where(ProductModel.id==UUID(product_data.product_id))).first()
    if not product_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product not found")
    
    stock = session.exec(select(StockLevel).where(StockLevel.product_id == UUID(product_data.product_id))).first()
    if not stock:
        stock = StockLevel(product_id=UUID(product_data.product_id), current_stock=0)
        session.add(stock)
    stock.current_stock += int(product_data.quantity)
    stock.product = product_exist
    stock.updated_at = datetime.now(timezone.utc)

    product_exist.stock = stock
    product_exist.updated_at = datetime.now(timezone.utc)

    stock_info = stock.model_copy()
    transaction = InventoryTransaction(stock_id=stock_info.id, product_id=product_exist.id, quantity=int(product_data.quantity), operation=Operation.ADD, stock=stock, product=product_exist)
    
    stock.transactions.append(transaction)
    product_exist.transactions.append(transaction)

    session.add(transaction)
    session.commit()
    session.refresh(product_exist)
    session.refresh(stock)
    session.refresh(transaction)

    return {"message": "Stock added successfully", "transaction": transaction, "product_exist": product_exist, "stock": stock } 

@router.post("/subtract-inventory")
async def subtract_inventory(product_data: InventorySubtractReq, session: Annotated[Session, Depends(get_session)]):
    product_exist = session.exec(select(ProductModel).where(ProductModel.id==UUID(product_data.product_id))).first()
    if not product_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product not found")
    
    stock = session.exec(select(StockLevel).where(StockLevel.product_id == UUID(product_data.product_id))).first()
    if not stock:
        stock = StockLevel(product_id=UUID(product_data.product_id), current_stock=0)
        session.add(stock)
    
    if stock.current_stock < int(product_data.quantity):
        raise HTTPException(status_code=400, detail="Insufficient stock")

    stock.current_stock -= int(product_data.quantity)
    stock.updated_at = datetime.now(timezone.utc)
    
    transaction = InventoryTransaction(stock_id=stock.id, product_id=product_exist.id, quantity=int(product_data.quantity), operation=Operation.SUBTRACT)
    
    stock.transactions.append(transaction)
    product_exist.transactions.append(transaction)
    
    product_exist.updated_at = datetime.now(timezone.utc)

    session.add(transaction)
    session.commit()
    session.refresh(product_exist)
    session.refresh(stock)
    return {"message": "Stock Subtract successfully", "product": product_exist, "stock": stock} 

@router.get("/get-all-stocks", response_model=list[StockLevelSchema])
async def all_stocks(session: Annotated[Session, Depends(get_session)]):
    stock = session.exec(select(StockLevel)).all()
    return stock

@router.get("/get-all-inventory-transactions", response_model=list[InventoryTransactionSchema])
async def all_transactions(session: Annotated[Session, Depends(get_session)]):
    inventory = session.exec(select(InventoryTransaction)).all()
    return inventory

@router.get("/get-inventory-transactions-by-product-id", response_model=list[InventoryTransactionSchema])
async def transactions_by_product_id(product_id: str ,session: Annotated[Session, Depends(get_session)]):
    transactions = session.exec(select(InventoryTransaction).where(InventoryTransaction.product_id==UUID(product_id))).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product's transactions not found")
    return transactions

@router.get("/get-stock-by-product-id", response_model=list[StockLevelSchema])
async def stocks_by_product_id(product_id: str ,session: Annotated[Session, Depends(get_session)]):
    stocks = session.exec(select(StockLevel).where(StockLevel.product_id==UUID(product_id))).all()
    if not stocks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product's stock not found")
    return stocks
















    # return {"product_data": product_data, "product_exist": product_exist, "inventory": inventory} 

    # new_product = productModel(first_name=product.first_name, last_name=product.last_name, password=product.password, email=product.email)
    # product_protobuf = mart_pb2.Product(id=str(ready_product.id), name= ready_product.name, price=ready_product.price, category= ready_product.category, quantity= ready_product.quantity)
    # serialized_product = product_protobuf.SerializeToString()
    # protobuf_product = product_pb2.product()
    # producer.send_and_wait("")