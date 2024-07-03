# from fastapi import APIRouter, HTTPException, status, Depends
# from sqlmodel import SQLModel, select, Session
# from app.schemas.user import UserReq, UserRes
# from app.models.user import UserModel
# from app.config.kafka import get_producer
# from app.config.database import get_session
# from aiokafka import AIOKafkaProducer
# from typing import Annotated
# from app.protobuf import user_pb2

# router = APIRouter(prefix="/user", tags=["User Auth"], responses={404:{"description": "Not found"}})

# @router.post("/register")
# async def create_user(user: UserReq, session: Annotated[Session, Depends(get_session)]):#, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]):
#     user_exist = session.exec(select(UserModel).where(UserModel.email==user.email)).first()
#     if user_exist:
#         if user_exist.is_verified:
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user '{user.email}' is already exist")
#         # send email
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user '{user.email}' is not verified, we have sent you an email, please check and verify")
    
#     # new_user = UserModel(first_name=user.first_name, last_name=user.last_name, password=user.password, email=user.email)
#     # product_protobuf = mart_pb2.Product(id=str(ready_product.id), name= ready_product.name, price=ready_product.price, category= ready_product.category, quantity= ready_product.quantity)
#     # serialized_product = product_protobuf.SerializeToString()
#     # protobuf_product = user_pb2.User()
#     # producer.send_and_wait("")
#     return True 
