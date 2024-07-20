from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import PRODUCT_DATABASE_URL
from contextlib import asynccontextmanager
from app.services.kafka.consumer import kafka_consumer
from fastapi import FastAPI
import asyncio

connection_str = str(PRODUCT_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    # create_database("mytestdatabase")
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("product-added"))
    asyncio.create_task(kafka_consumer("product-and-inventory-added"))
    asyncio.create_task(kafka_consumer("product_updated"))
    # asyncio.create_task(kafka_consumer("product_product_product_updated"))
    print("table created")
    yield