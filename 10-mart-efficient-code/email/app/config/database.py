from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import DATABASE_URL
from contextlib import asynccontextmanager
from app.services.kafka.consumer import kafka_consumer
from fastapi import FastAPI
import asyncio
connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("email-to-unverified-user-topic"))
    asyncio.create_task(kafka_consumer("email-to-new-user-topic"))
    asyncio.create_task(kafka_consumer("email-to-reset-password-user-topic"))
    asyncio.create_task(kafka_consumer("email-verify-reset-password-user-topic"))
    asyncio.create_task(kafka_consumer("email-to-new-verified-user-topic"))
    
    asyncio.create_task(kafka_consumer("email-to-new-company-topic"))
    asyncio.create_task(kafka_consumer("email-to-unverified-company-topic"))
    asyncio.create_task(kafka_consumer("email-to-new-verify-company-topic"))
    asyncio.create_task(kafka_consumer("email-to-reset-password-company-topic"))

    asyncio.create_task(kafka_consumer("inventory-email-transaction-added"))
    asyncio.create_task(kafka_consumer("product-email-product-added"))
    asyncio.create_task(kafka_consumer("product-email-product-updated"))
    
    print("table created")
    yield