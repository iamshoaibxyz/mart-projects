from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from app.services.kafka.consumer import kafka_consumer
from app.config.settings import ORDER_DATABASE_URL

connection_str = str(ORDER_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    SQLModel.metadata.create_all(engine) # order_added
    asyncio.create_task(kafka_consumer("order_added"))
    asyncio.create_task(kafka_consumer("orders_added"))
    
    print("table created")
    yield