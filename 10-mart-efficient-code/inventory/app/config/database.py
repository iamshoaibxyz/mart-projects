from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import DATABASE_URL
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.kafka.consumer import kafka_consumer
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
    asyncio.create_task(kafka_consumer("product-inventory-stock-added"))
    print("table created")
    yield