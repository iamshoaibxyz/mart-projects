from contextlib import asynccontextmanager
from app.services.kafka.consumer import kafka_consumer
from fastapi import FastAPI
import asyncio

# connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")

# engine = create_engine(connection_str)

# async def get_session():
#     with Session(engine) as session:
#         yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    # SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("email-user-added"))
    asyncio.create_task(kafka_consumer("email-verification-to-unverified-user"))
    asyncio.create_task(kafka_consumer("email-user-verified-updated"))
    asyncio.create_task(kafka_consumer("email-user-reset-password"))
    asyncio.create_task(kafka_consumer("email-user-password-updated"))
    asyncio.create_task(kafka_consumer("email-user-deleted"))
      
    asyncio.create_task(kafka_consumer("email-company-added"))
    asyncio.create_task(kafka_consumer("email-verification-to-unverified-company"))
    asyncio.create_task(kafka_consumer("email-company-verified-updated"))
    asyncio.create_task(kafka_consumer("email-company-reset-password"))
    asyncio.create_task(kafka_consumer("email-company-info-updated"))
    asyncio.create_task(kafka_consumer("email-company-deleted"))

    asyncio.create_task(kafka_consumer("email-product-added"))
    
    asyncio.create_task(kafka_consumer("email-transaction-subtracted"))
    asyncio.create_task(kafka_consumer("email-transaction-added"))
    # asyncio.create_task(kafka_consumer("inventory-email-transaction-added"))
    # asyncio.create_task(kafka_consumer("product-email-product-updated"))
    
    print("table created")
    yield