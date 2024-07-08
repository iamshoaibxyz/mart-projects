from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
# from app.services.database.session import get_session
from sqlmodel import Session, create_engine, select
from app.utils.proto_utils import  proto_to_productmodel, product_to_proto
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.all_models import CompanyModel, ProductModel
from uuid import UUID

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def add_new_product(product_proto):
    new_product = proto_to_productmodel(product_proto)
    async with get_session() as session:
        company = session.get(CompanyModel, new_product.company_id)
        company.products.append(new_product)
        session.add(company)
        session.commit() 
        session.refresh(company)
    async with get_producer() as producer:
        # proto_product = product_to_proto(new_product)
        await producer.send_and_wait("email-to-new-product-topic", product_proto.SerializeToString())

# async def verify_new_company(company_proto):
#     company_model = proto_to_company(company_proto)
#     async with get_session() as session:
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
#         await producer.send_and_wait("email-to-new-verify-company-topic", proto_company.SerializeToString())
