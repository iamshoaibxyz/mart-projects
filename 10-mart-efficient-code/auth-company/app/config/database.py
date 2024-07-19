from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import COMPANY_DATABASE_URL
from contextlib import asynccontextmanager
from app.services.kafka.consumer import kafka_consumer
from fastapi import FastAPI
import asyncio

connection_str = str(COMPANY_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("company-added"))
    asyncio.create_task(kafka_consumer("company-verify-updated"))
    asyncio.create_task(kafka_consumer("company-token-added"))
    asyncio.create_task(kafka_consumer("company-password-updated"))
    asyncio.create_task(kafka_consumer("company-updated"))
    asyncio.create_task(kafka_consumer("company-deleted"))
    print("table created")
    yield