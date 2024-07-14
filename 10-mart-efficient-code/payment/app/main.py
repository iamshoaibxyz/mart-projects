from uuid import UUID
from fastapi import Depends, FastAPI, Request
from requests import Session
from app.config.settings import STRIPE_API_KEY
from app.config.database import get_session
from stripe.webhook import Webhook
from fastapi import HTTPException
from typing import List, Annotated
import stripe

stripe.api_key = STRIPE_API_KEY


app : FastAPI = FastAPI(servers=[{"url":"http://127.0.0.1:8007"}])

@app.get("/")
def root():
    return {"message": "Payment soursecode"}


@app.get("/success")
def root():
    return {"message": "Payment success"}


@app.get("/cancel")
def root():
    return {"message": "Payment cancel"}

@app.post("/payment")
def payment(session: Annotated[Session, Depends(get_session)]):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': "usd",
                    'product_data': {
                        'name': f"product a ",
                    },
                    'unit_amount':  1000,  # Amount in cents
                },
                'quantity': 2,
            }],
            mode='payment',
            success_url="http://127.0.0.1:8007/success",
            cancel_url="http://127.0.0.1:8007/cancel",
        )
        return session
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# def create_stripe_session(cart_id: UUID, total_amount: int, currency: str, success_url: str, cancel_url: str):
#     try:
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': currency,
#                     'product_data': {
#                         'name': f"Cart {cart_id}",
#                     },
#                     'unit_amount': total_amount,
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url=success_url,
#             cancel_url=cancel_url,
#         )
#         return session
#     except stripe.error.StripeError as e:
#         raise HTTPException(status_code=400, detail=str(e))
 
# @app.post("/create-payment-session/{cart_id}")
# async def create_payment_session(cart_id: UUID, session: Session = Depends(get_session)):
#     # cart = session.exec(select(CartModel).where(CartModel.id == cart_id)).first()
#     if not cart:
#         raise HTTPException(status_code=404, detail="Cart not found")

#     # Calculate the total amount from the cart's orders
#     total_amount = sum(order.total_price for order in cart.orders)

#     session_url = create_stripe_session(
#         cart_id=cart.id,
#         total_amount=int(total_amount * 100),  # Convert to cents
#         currency="usd",
#         success_url="https://yourdomain.com/success",
#         cancel_url="https://yourdomain.com/cancel"
#     )

#     return {"checkout_url": session_url.url}


# @app.post("/webhook")
# async def stripe_webhook(request: Request):
#     payload = await request.body()
#     sig_header = request.headers.get('stripe-signature')
#     event = None

#     try:
#         event = Webhook.construct_event(payload, sig_header, "your_webhook_secret")
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail="Invalid payload")
#     except stripe.error.SignatureVerificationError as e:
#         raise HTTPException(status_code=400, detail="Invalid signature")

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         handle_successful_payment(session)

#     return {"message": "Received"}
 