from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
# from app.services.database.session import get_session
from sqlmodel import Session, create_engine, select
from app.utils.proto_utils import proto_to_company, company_to_proto ,email_content_to_proto, email_to_proto, proto_to_email, proto_to_email_content, proto_to_usermodel
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.all_models import UserModel
from app.config.email import send_mail
from app.config.security import hashed_url

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session



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
            email: {email}
            token: {token_url}
            {name.capitalize()} was not verified, this token will help you to verify the company
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
            token: {token}
            email: {email}
            This is the email for the reset password, copy and past if on verify-reset route, and set new password to your company ... 
"""
    await send_mail(email=email, html=html)


# async def verify_new_user(user_proto):
#     user_model = proto_to_usermodel(user_proto)
#     async with get_session() as session:
#         user = session.get(UserModel, user_model.id)
#         user.is_verified = True
#         user.verified_at = datetime.now(timezone.utc)
#         user.updated_at = datetime.now(timezone.utc)
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#     # send to kafka and then email-service will be recived
#     async with get_producer() as producer:
#         proto_user = user_to_proto(user)
#         await producer.send_and_wait("send-email-to-new-verify-user-topic", proto_user.SerializeToString())

# async def user_token(proto_user_token):
#     user_token: UserTokenModel = proto_to_user_token(proto_user_token)
#     async with get_session() as session:
#         user: UserModel = session.get(UserModel, user_token.user_id)
#         user.tokens.append(user_token)
#         session.add(user)
#         session.commit()
#         session.refresh(user)
# async def register_new_company(company_proto):
#     new_company = proto_to_company(company_proto)
#     async with get_session() as session:
#         session.add(new_company)
#         session.commit()
#         session.refresh(new_company)
#     # send to kafka and then email recived then send to company email for verification
#     async with get_producer() as producer:
#         proto_company = company_to_proto(new_company)
#         await producer.send_and_wait("send-email-to-new-company-topic", proto_company.SerializeToString())

# async def verify_new_company(company_proto):
#     company_model = proto_to_company(company_proto)
#     async with get_session() as session:
#         # company = session.exec(select(CompanyModel).where(CompanyModel.id==company_model.id)).first()
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
#         await producer.send_and_wait("send-email-to-new-verify-company-topic", proto_company.SerializeToString())

# async def company_token(proto_company_token):
#     company_token = proto_to_company_token(proto_company_token)
#     async with get_session() as session:
#         company = session.get(CompanyModel, company_token.company_id)
#         company.tokens.append(company_token)
#         session.add(company)
#         session.commit()


















# connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
# engine = create_engine(connection_str)
    # async def get_session():
    #     with Session(engine) as session:
    #         yield session