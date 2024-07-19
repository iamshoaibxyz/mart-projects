from contextlib import asynccontextmanager
from app.config.settings import COMPANY_DATABASE_URL
from sqlmodel import Session, create_engine
from app.utils.proto_conversion import  proto_to_company_token, proto_to_company, company_to_proto
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.company import  CompanyModel

connection_str = str(COMPANY_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
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
    async with get_producer() as producer:
        proto_company = company_to_proto(new_company)
        await producer.send_and_wait("email-company-added", proto_company.SerializeToString())

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
    async with get_producer() as producer:
        await producer.send_and_wait("email-company-verified-updated", company_proto.SerializeToString())
 
async def company_token(proto_company_token):
    company_token = proto_to_company_token(proto_company_token)
    async with get_session() as session:
        session.add(company_token)
        company = session.get(CompanyModel, company_token.company_id)
        company_token.company = company
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
    async with get_producer() as producer:
        await producer.send_and_wait("email-company-info-updated", proto_company.SerializeToString())
 

async def delete_company(proto_company):
    company_model = proto_to_company(proto_company)
    async with get_session() as session:
        company: CompanyModel = session.get(CompanyModel, company_model.id)
        session.delete(company)
        session.commit()
    async with get_producer() as producer:
        await producer.send_and_wait("email-company-deleted", proto_company.SerializeToString())
 