from typing import Annotated
from uuid import uuid4, UUID
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
from sqlalchemy import create_engine, select
import stripe
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel, Session

# class Order(SQLModel):
#     product_id: UUID
#     quantity: int

# class OrderPlace(Order, table=True):
#     order_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)    
#     product_price: int
#     product_name: str
#     product_category: str
#     totle_price: int
    
DATABASE_URL="postgresql://shoaib:mypassword@postgresCont:5432/mydatabase"
connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")

# def get_session():
#     with Session(engine) as session:
#         yield session

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     print("Creating table")
#     SQLModel.metadata.create_all(engine)
#     print("table Created")
#     yield

# This is your test secret API key.
stripe.api_key = 'sk_test_51PQwQtIf22jmWnXxgTSFMFUHxW75nkwV9kwyT6g1U62kxv65cneW5XUs0QbLbVAkB4RmBf9lh7SOB5nDC0apqWsL00DyRI6fF2'

app = FastAPI(title="Payment Mart", servers=[{
    "url": "http://127.0.0.1:8003",
    "description": "Development server"
}])

# Mount the static directory
app.mount("/Frontend", StaticFiles(directory="Frontend"), name="Frontend")

YOUR_DOMAIN = 'http://127.0.0.1:8003'

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# @app.get("/orderid")#session: Annotated[Session, Depends(get_session)]
# def get_order(orderid, ):
    
#     with Session(engine) as session:
#         order = session.exec(select(OrderPlace)).all()
#         return order
#     # return orderid

@app.get("/checkout.html", response_class=HTMLResponse)
async def get_checkout():
    with open('Frontend/checkout.html', 'r') as f:
        checkout_html = f.read()
    return Response(content=checkout_html, media_type="text/html")

@app.get("/success.html", response_class=HTMLResponse)
async def get_success():
    with open('Frontend/success.html', 'r') as f:
        success_html = f.read()
    return Response(content=success_html, media_type="text/html")

@app.get("/cancel.html", response_class=HTMLResponse)
async def get_cancel():
    with open('Frontend/cancel.html', 'r') as f:
        cancel_html = f.read()
    return Response(content=cancel_html, media_type="text/html")


@app.post('/create-checkout-session')
async def create_checkout_session(order_id: str):
    try:
        # Example inter-service call to api-service
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://martCont:8000/order/get_orders_by_id?order_id={order_id}')
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error in api-service call")
            product = response.json()

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1PShL1If22jmWnXxW8BRw0jI',
                    'quantity': product.quantity,
                    'name': product.product_name,
                    'amount': product.product_price,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return {"url": checkout_session.url, "product": product}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

