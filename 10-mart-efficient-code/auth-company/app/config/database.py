from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import DATABASE_URL
from contextlib import asynccontextmanager
from app.services.kafka.consumer import kafka_consumer
from fastapi import FastAPI
import asyncio
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

def create_database(dbname):
    conn = psycopg2.connect(
        dbname="mydatabase",  # Connect to the default database
        user="shoaib",
        password="mypassword",
        host="postgresContainer"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {dbname};")
    cursor.close()
    conn.close()

# with engine.connect() as conn:
#     # conn.execute("commit")  # Necessary to commit the next transaction
#     conn.execute("CREATE DATABASE mytestdatabase")

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    # create_database("mytestdatabase")
    SQLModel.metadata.create_all(engine)
    # asyncio.create_task(kafka_consumer("hello"))
    # asyncio.create_task(kafka_consumer("register-new-user-topic"))
    # asyncio.create_task(kafka_consumer("verify-new-user-topic"))
    asyncio.create_task(kafka_consumer("delete-company"))
    asyncio.create_task(kafka_consumer("register-new-company-topic"))
    asyncio.create_task(kafka_consumer("verify-new-company-topic"))
    asyncio.create_task(kafka_consumer("company-token-topic"))
    asyncio.create_task(kafka_consumer("verify-reset-password-company-topic"))
    asyncio.create_task(kafka_consumer("update-company-topic"))
    print("table created")
    yield