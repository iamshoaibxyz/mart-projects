from contextlib import asynccontextmanager
from app.config.settings import DATABASE_URL
from sqlmodel import Session, create_engine, select
from app.utils.proto_conversion import proto_to_user, user_to_proto, proto_to_user_token
from app.services.kafka.producer import get_producer
from datetime import datetime, timezone
from app.models.user import UserModel, UserTokenModel

connection_str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def get_session(): 
    with Session(engine) as session:
        yield session

async def register_new_user(user_proto):
    new_user = proto_to_user(user_proto)
    async with get_session() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    async with get_producer() as producer:
        await producer.send_and_wait("email-user-added", user_proto.SerializeToString())

async def verify_new_user(user_proto):
    user_model = proto_to_user(user_proto)
    async with get_session() as session:
        user = session.get(UserModel, user_model.id)
        user.is_verified = True
        user.verified_at = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)
        session.add(user)
        session.commit()
        session.refresh(user)
    # send to kafka and then email-service will be recived
    async with get_producer() as producer:
        await producer.send_and_wait("email-user-verified-updated", user_proto.SerializeToString())
 
async def user_token(proto_user_token):
    user_token = proto_to_user_token(proto_user_token)
    async with get_session() as session:
        session.add(user_token)
        user: UserModel = session.get(UserModel, user_token.user_id)
        user_token.user = user
        user.tokens.append(user_token)
        session.add(user)
        session.commit()
        session.refresh(user)
        

async def verify_reset_password_user(proto_user):
    user_model = proto_to_user(proto_user)
    async with get_session() as session:
        user: UserModel = session.get(UserModel, user_model.id)
        user.password = user_model.password
        user.updated_at = user_model.updated_at
        session.add(user)
        session.commit()
        session.refresh(user)
    async with get_producer() as producer:
        await producer.send_and_wait("email-user-password-updated", proto_user.SerializeToString())

async def delete_user(proto_user):
    user_model = proto_to_user(proto_user)
    async with get_session() as session:
        user = session.get(UserModel, user_model.id)
        session.delete(user)
        session.commit()
    async with get_producer() as producer:
        await producer.send_and_wait("email-user-deleted", proto_user.SerializeToString())

