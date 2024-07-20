from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select, Session
from typing import Annotated
from uuid import UUID

from app.models.order import OrderPlacedModel, CartModel, OrderStatus
from app.schemas.order import OrderReq, MultiOrderReq
from app.schemas.protos import order_pb2
from app.utils.proto_conversion import order_to_proto
from app.config.database import get_session
from app.services.kafka.producer import get_producer
from app.utils.fetcher import auth_checker, fetch_product_detail_by_id, fetch_stock_detail_by_product_id

oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8001/user/user-login")

router = APIRouter(prefix="/order", tags=["Order"], responses={404:{"description": "Not found"}})
# order_data: OrderReq
@router.post("/order-place")
async def order_place(product_id: UUID, quantity: Annotated[int, Query(..., ge=1, lt=99)], session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
    user = await auth_checker(token=token)
    product = await fetch_product_detail_by_id(str(product_id))
    stock = await fetch_stock_detail_by_product_id(str(product_id))
    if int(stock.get("current_stock")) < quantity:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Insufficient stock")
    order = OrderPlacedModel(
        cart_id=UUID(user.get("id")),
        user_id=UUID(user.get("id")),
        product_id=UUID(product.get("id")),
        product_price=float(product.get("price")),
        total_price=float(product.get("price")) * quantity,
        quantity=quantity,
        status="initialized" # OrderStatus
    )
    order_proto = order_to_proto(order)
    async with get_producer() as producer:
        await producer.send_and_wait("order_added", order_proto.SerializeToString())
    return { "message": "order successfuly added", "user": user, "product": product, "stock": stock, "order": order}















# @router.post("/order")
# async def place_single_order(order_data: OrderReq, session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
#     try:
#         user = user_auth_checker(session, token)
#         product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id==UUID(order_data.product_id))).first()
#         if not product:
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"product not found")
#         stock = session.exec(select(StockLevel).where(StockLevel.product_id==product.id)).first()
#         if not stock:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is an invalid stock")
#         if stock.current_stock < int(order_data.quantity):  
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"insufficient stock, there is just only '{stock.current_stock}' items avaliable ")
#         cart = CartModel(
#             user_id=user.id, 
#             total_price=float(product.price * int(order_data.quantity))
#             )
#         session.add(cart)
#         order = OrderPlacedModel(
#             user_id=user.id, 
#             quantity=order_data.quantity, 
#             product_id=UUID(order_data.product_id), 
#             product_price=product.price,
#             cart_id=cart.id,
#             total_price=float(product.price * int(order_data.quantity))
#               )
#         order.cart_id = cart.id
        
#         session.add(order)

#         order.user = user
#         order.product = product

#         cart.orders.append(order)
#         product.orders.append(order)
#         user.carts.append(cart)
#         user.orders.append(order)


#         return {user, product, cart, order} 
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 
# @router.post("/order")
# async def place_single_order(order_data: OrderReq, session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
#     try:
#         user = user_auth_checker(session, token)
#         product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id == UUID(order_data.product_id))).first()
#         if not product:
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"product not found")
#         stock = session.exec(select(StockLevel).where(StockLevel.product_id == product.id)).first()
#         if not stock:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is an invalid stock")
#         if stock.current_stock < int(order_data.quantity):
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"insufficient stock, there is just only '{stock.current_stock}' items available")

#         # Start transaction block
#         with session.begin():
#             cart = CartModel(
#                 user_id=user.id, 
#                 total_price=float(product.price * int(order_data.quantity))
#             )
#             session.add(cart)
#             session.flush()  # Ensure cart_id is available for order

#             order = OrderPlacedModel(
#                 user_id=user.id, 
#                 quantity=order_data.quantity, 
#                 product_id=UUID(order_data.product_id), 
#                 product_price=product.price,
#                 cart_id=cart.id,
#                 total_price=float(product.price * int(order_data.quantity))
#             )
#             session.add(order)

#             # Add relationships
#             order.user = user
#             order.product = product
#             cart.orders.append(order)
#             product.orders.append(order)
#             user.carts.append(cart)
#             user.orders.append(order)

#         # session.commit()  # Commit the transaction

#         return {"user": user, "product": product, "cart": cart, "order": order}
#     except Exception as e:
#         session.rollback()  # Rollback the transaction in case of error
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# router = APIRouter()

# Define the route for placing a single order
# @router.post("/order")
# async def place_single_order( order_data: OrderReq, session: Session = Depends(get_session), token: dict = Depends(oauth2_user_scheme) ):
#     try:
#         # Authenticate the user
#         user = user_auth_checker(session, token)
        
#         # Get the product from the database
#         product = session.exec(select(ProductModel).where(ProductModel.id == UUID(order_data.product_id))).first()
#         if not product:
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Product not found")
        
#         # Get the stock level for the product
#         stock = session.exec(select(StockLevel).where(StockLevel.product_id == product.id)).first()
#         if not stock:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stock")
        
#         # Check if there is sufficient stock
#         if stock.current_stock < int(order_data.quantity):
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Insufficient stock, only '{stock.current_stock}' items available")
        
#         # # Create the cart and order
#         cart = CartModel(
#             user_id=user.id,
#             total_price=float(product.price * int(order_data.quantity))
#         )
        
#         # Add and flush the cart to get the cart_id
#         # session.add(cart)
#         # session.flush()  # Ensure cart_id is available for order

#         # Create the order and link it to the cart
#         order = OrderPlacedModel(
#             user_id=user.id,
#             quantity=order_data.quantity,
#             product_id=UUID(order_data.product_id),
#             product_price=product.price,
#             cart_id=cart.id,  # Set cart_id after flushing
#             status="initialized",
#             total_price=float(product.price * int(order_data.quantity))
#         )

#         order.user = user
#         order.product = product
#         order.cart = cart

#         cart.user = user
#         cart.orders.append(order)

#         session.add(cart)
#         session.add(order)

        # # Update relationships
        # product.orders.append(order)
        # user.carts.append(cart)
        # user.orders.append(order)

        # # Commit the transaction
        # session.commit()
        # session.refresh(order)
        # session.refresh(cart)
        # session.refresh(product)
        # session.refresh(user)

#         return {"user": 'user, "order": order, "cart": cart'}
#     except Exception as e:
#         session.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 
# @router.post("/multi-orders")
# async def multi_single_order(orders_data: MultiOrderReq, session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
#     try:
        # user = user_auth_checker(session, token)
        # product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id==UUID(order_data.product_id))).first()
        # if not product:
        #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"product not found")
        # stock = session.exec(select(StockLevel).where(StockLevel.product_id==product.id)).first()
        # if not stock:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is an invalid stock")
        # if stock.current_stock < int(order_data.quantity):  
        #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"insufficient stock, there is just only '{stock.current_stock}' items avaliable ")
        # order = OrderPlacedModel(
        #     user_id=user.id, 
        #     quantity=order_data.quantity, 
        #     product_id=UUID(order_data.product_id), 
        #     product_price=product.price, 
        #     total_price=float(product.price * int(order_data.quantity))
        #       )
        # cart = CartModel(
        #     user_id=user.id, 
        #     total_price=float(product.price * int(order_data.quantity))
        #     )
        
        # session.add(order)
        # session.add(cart)

        # order.cart_id = cart.id
        # order.user = user
        # order.product = product

        # cart.orders.append(order)
        # product.orders.append(order)
        # user.carts.append(cart)
        # user.orders.append(order)


        # # async with get_producer as producer:
        # #     producer.send_and_wait("order-placed", )
        # return {cart ,order, product, product} 
    #     return {orders_data} 
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 

# @router.get("/get-orders")
# async def place_single_order(session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
#     user = user_auth_checker(session, token)        
#     # Get the product from the database
#     orders = session.exec(select(OrderPlacedModel).where(OrderPlacedModel.user_id == user.id )).all()
#     if not orders:
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="orders not found")
#     return orders

# @router.get("/get-carts")
# async def place_single_order(session: Annotated[Session, Depends(get_session)], token: Annotated[dict, Depends(oauth2_user_scheme)]):
#     user = user_auth_checker(session, token)        
#     # Get the product from the database
#     orders = session.exec(select(CartModel).where(CartModel.user_id == user.id )).all()
#     if not orders:
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="orders not found")
#     return orders


# @router.get("/orderplace")
# def order_place():
#     order = OrderPlacedModel(
#             user_id=UUID("2d46765a-bea2-4ab7-9a56-4ef489d56e6f"),
#             quantity=6,
#             product_id=UUID("2d46765a-bea2-4ab7-9a56-4ef489d56e6f"),
#             product_price=5,
#             cart_id=UUID("2d46765a-bea2-4ab7-9a56-4ef489d56e6f"),  # Set cart_id after flushing
#             status=OrderStatus.INITIALIZED.value,
#             total_price=float(2.1 * int(5))
#         )
#     return order
