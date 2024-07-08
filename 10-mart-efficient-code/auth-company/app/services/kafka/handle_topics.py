from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
# from app.services.database.session import get_session
from sqlmodel import Session, create_engine, select
from app.utils.proto_utils import proto_to_usermodel, user_to_proto, proto_to_user_token, proto_to_company, company_to_proto, proto_to_company_token
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.all_models import UserModel, UserTokenModel, CompanyModel
from uuid import UUID

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def register_new_company(company_proto):
    new_company = proto_to_company(company_proto)
    async with get_session() as session:
        session.add(new_company)
        session.commit() 
        session.refresh(new_company)
    # send to kafka and then email recived then send to company email for verification
    async with get_producer() as producer:
        proto_company = company_to_proto(new_company)
        await producer.send_and_wait("email-to-new-company-topic", proto_company.SerializeToString())

async def verify_new_company(company_proto):
    company_model = proto_to_company(company_proto)
    async with get_session() as session:
        company = session.get(CompanyModel, company_model.id)
        company.is_verified = True
        company.verified_at = datetime.now(timezone.utc)
        company.updated_at = datetime.now(timezone.utc)
        session.add(company)
        session.commit()
        session.refresh(company)
    # send to kafka and then email-service will be recived
    async with get_producer() as producer:
        proto_company = company_to_proto(company)
        await producer.send_and_wait("email-to-new-verify-company-topic", proto_company.SerializeToString())

async def company_token(proto_company_token):
    company_token = proto_to_company_token(proto_company_token)
    async with get_session() as session:
        company = session.get(CompanyModel, company_token.company_id)
        company.tokens.append(company_token)
        session.add(company)
        session.commit()

async def verify_reset_password_company(proto_company):
    company_model = proto_to_company(proto_company)
    async with get_session() as session:
        company: CompanyModel = session.get(CompanyModel, company_model.id)
        company.password = company_model.password
        company.updated_at = company_model.updated_at
        session.add(company)
        session.commit()
        session.refresh(company)

async def update_company(proto_company):
    company_model = proto_to_company(proto_company)
    async with get_session() as session:
        company: CompanyModel = session.get(CompanyModel, company_model.id)
        company.name = company_model.name
        company.email = company_model.email
        company.description = company_model.description
        session.add(company)
        session.commit()
        session.refresh(company)
