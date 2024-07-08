from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
# from app.services.database.session import get_session
from sqlmodel import Session, create_engine, select
from app.utils.proto_utils import product_to_proto, proto_to_productmodel, proto_to_company, company_to_proto ,email_content_to_proto, email_to_proto, proto_to_email, proto_to_email_content, proto_to_usermodel
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.all_models import UserModel, ProductModel, CompanyModel
from app.config.email import send_mail
from app.config.security import hashed_url

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session



# =================================user==================================

async def email_to_unverified_user(user_proto):
    user = proto_to_usermodel(user_proto)
    context = str(user.get_context_str())
    hasded = hashed_url(context)
    email = user.email
    html = f"""
            token: {hasded}
            email: {email}
            This is the email for the old user verification.
            """
    await send_mail(email=email, html=html)

async def email_to_new_user(user_proto): 
    user = proto_to_usermodel(user_proto)
    context = str(user.get_context_str())
    hasded = hashed_url(context)
    email = user.email
    html = f"""
            token: {hasded}
            email: {email}
            This is the email for the new user verification.
            """
    await send_mail(email=email, html=html)

async def email_to_reset_password_user(user_proto):
    user_model: UserModel = proto_to_usermodel(user_proto)
    verify_context = user_model.get_context_str("VERIFY_USER_CONTEXT")
    token_url = hashed_url(verify_context)
    email = user_model.email
    html = f"""
            token: {token_url}
            email: {email}
            This is the email for the reset password ... 
"""
    await send_mail(email=email, html=html)

async def email_verify_reset_user_password(user_proto):
    user_model: UserModel = proto_to_usermodel(user_proto)
    
    email = user_model.email
    html = f"""
            email: {email}
            Your password has been successfully changed, now you should procied to the login
"""
    await send_mail(email=email, html=html)


# =================================company==================================


async def email_to_new_company(company_proto):
    company = proto_to_company(company_proto)
    context = str(company.get_context_str())
    token = hashed_url(context)
    email = company.email
    name = company.name
    html = f"""
            email: {email}
            token: {token}
            {name.capitalize()} is successfully registered, copy the token and past it to reset-verify route
"""
    await send_mail(email=email, html=html)
    

async def verify_email_to_new_company(company_proto):
    company = proto_to_company(company_proto)
    email = company.email
    name = company.name
    html = f"""
            email: {email} <br/>
            Congratulation '{name.capitalize()}' is successfully verified
"""
    await send_mail(email=email, html=html)
    

async def email_to_unverified_company(company_proto):
    company_model = proto_to_company(company_proto)
    url_context = company_model.get_context_str()
    token_url = hashed_url(url_context)
    email = company_model.email
    name = company_model.name
    html = f"""
            email: '{email}'
            token: '{token_url}'
            '{name.capitalize()}' was not verified, this token will help you to verify the company
"""
    await send_mail(email=email, html=html)
    
    





















    # async with get_session() as session:
    #     session.add(new_user)
    #     session.commit()
    #     session.refresh(new_user)
    # send to kafka and then email-service will be recived
    # async with get_producer() as producer:
    #     proto_user = user_to_proto(new_user)
    #     await producer.send_and_wait("send-email-to-new-user-topic", proto_user.SerializeToString())


async def email_to_reset_password_company(company_proto):
    company = proto_to_company(company_proto)
    verify_context = company.get_context_str("VERIFY_COMPANY_CONTEXT")
    token = hashed_url(verify_context)
    email = company.email
    html = f"""
            token: '{token}'
            email: '{email}'
            This is the email for the reset password, copy and past if on verify-reset route, and set new password to your company ... 
"""
    await send_mail(email=email, html=html)


# =================================product==================================

async def email_to_new_product_company(product_proto):
    product = proto_to_productmodel(product_proto)
    async with get_session() as session: 
        company: CompanyModel = session.get(CompanyModel, product.company_id)
        email = company.email
        html = f"""
                email: '{email}'
                Congratulation product '{product.name.capitalize*()}' is successfully added by '{company.name.capitalize()}'  Company, please add inventory related detail"""
        await send_mail(email=email, html=html)

