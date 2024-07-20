from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from app.services.kafka.consumer import kafka_consumer
from app.config.settings import INVENTORY_DATABASE_URL

connection_str = str(INVENTORY_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    SQLModel.metadata.create_all(engine) 
    asyncio.create_task(kafka_consumer("inventory-added"))
    asyncio.create_task(kafka_consumer("inventory-subtracted"))
    asyncio.create_task(kafka_consumer("inventory-new-stock-added"))
    print("table created")
    yield