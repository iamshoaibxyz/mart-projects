from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, select, Session
from app.schemas.order import OrderReq 
from app.models.all_models import ProductModel, StockLevel, OrderPlacedModel
from app.config.kafka import get_producer
from app.config.database import get_session
from aiokafka import AIOKafkaProducer
from typing import Annotated
from app.protobuf import user_pb2
from uuid import UUID

from app.utils.check_auth import user_auth_checker

oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8001/user/user-login")

router = APIRouter(prefix="/order", tags=["Order"], responses={404:{"description": "Not found"}})

@router.post("/order")
async def create_user(order_data: OrderReq, session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
    try:
        user = user_auth_checker(session, token)
        product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id==UUID(order_data.product_id))).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"product not found")
        stock = session.exec(select(StockLevel).where(StockLevel.product_id==product.id)).first()
        if not stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is an invalid stock")
        if stock.current_stock < int(order_data.quantity):  
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"insufficient stock, there is just only '{stock.current_stock}' items avaliable ")
            # send email
        
        order = OrderPlacedModel(user_id=user.id, quantity=order_data.quantity, product_id=UUID(order_data.product_id), product_price=product.price, total_price=float(product.price * int(order_data.quantity)) )
        # async with get_producer as producer:
        #     producer.send_and_wait("order-placed", )
        return order 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
