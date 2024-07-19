from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import DATABASE_URL
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_str)

async def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("table creating")
    SQLModel.metadata.create_all(engine)
    print("table created")
    yield