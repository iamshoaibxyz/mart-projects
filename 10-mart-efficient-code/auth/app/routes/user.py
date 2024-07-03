from uuid import UUID
from app.config.security import hashed_password, verify_hashed_password, hashed_url, verify_hashed_url, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.user import UserReq, UserAccountVerifyReq, UserToken
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.validation import validate_password
from datetime import datetime, timedelta, timezone
from app.config.database import get_session
from app.models.all_models import UserModel, UserTokenModel
from app.services.kafka.producer import get_producer
from app.config.settings import TOKEN_EXPIRY
from sqlalchemy.orm import Session
from typing import Annotated, Any
from sqlmodel import select
from pydantic import EmailStr
from jwt.exceptions import PyJWTError
from app.utils.proto_utils import user_to_proto, user_token_to_proto

router = APIRouter(prefix="/user", tags=["User Auth"], responses={404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/user-login")

from app.schemas.user import UserSchema

@router.post("/register")
async def create_user(user: UserReq, session: Annotated[Session, Depends(get_session)]):
    user_exist = session.exec(select(UserModel).where(UserModel.email == user.email)).first()
    if user_exist:
        if user_exist.is_verified:
            return {"message": f"user '{user.email}' email is already registed and verified, please visit to login"}
        # Send email to user for verification
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user '{user.email}' is already exists, but not verified, we have sent you an email, please check and verify")
    validate_password(user.password)
    hash_password = hashed_password(user.password)
    new_user = UserModel(first_name=user.first_name, last_name=user.last_name, password=str(hash_password), email=user.email.lower())
    proto_user = user_to_proto(new_user)    
    async with get_producer() as producer:
        await producer.send_and_wait("register-new-user-topic", proto_user.SerializeToString())
    context_str = str(new_user.get_context_str())
    hash_url = hashed_url(context_str)
    return {"hashed_url": hash_url, "status": status.HTTP_201_CREATED, "message": "you have succcessfully signed up and we have send you an email, please check and verify"}

@router.post("/verify-user-account")
async def verify_user(user: UserAccountVerifyReq, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user_exist: UserModel = session.exec(select(UserModel).where(UserModel.email == user.email.lower())).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid creadential")
    context_str = str(user_exist.get_context_str())
    if not verify_hashed_url(context_str, user.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token eigther is invalid or expired")    
    proto_user = user_to_proto(user_exist)    
    async with get_producer() as producer:
        await producer.send_and_wait("verify-new-user-topic", proto_user.SerializeToString())

    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully verified, please visit to login"}

@router.post("/user-login")
async def user_login(user: Annotated[Any, Depends(OAuth2PasswordRequestForm)] , session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user_exist: UserModel = session.exec(select(UserModel).where(UserModel.email == user.username.lower())).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user '{user.username}' is not registered, please visit to signup and register to yourself")
    if not verify_hashed_password(user.password, user_exist.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid creadential")
    if not user_exist.is_verified:
        # send user verification email
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user '{user.username}' is not verified, we have send you and email, please check and verify to yourself")
    payload = {"id": str(user_exist.id), "first_name":user_exist.first_name, "last_name":user_exist.last_name, "email":user_exist.email}
    token = create_access_token(payload)
    token_expired_at= datetime.now(timezone.utc) + timedelta(minutes=float(TOKEN_EXPIRY))
    user_token = UserTokenModel(token=token, expired_at=token_expired_at, user_id=user_exist.id)
    proto_user_token = user_token_to_proto(user_token)
    async with get_producer() as producer:
        await producer.send_and_wait("user-token-topic", proto_user_token.SerializeToString())
        return UserToken(access_token=token, token_type="bearer", expires_in=str(token_expired_at)) # {"status": status.HTTP_200_OK, "message": "you have succcessfully login", "token": token, "user": user_exist}

@router.get("/get_all_users")
async def get_all_users(session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    users = session.exec(select(UserModel)).all()
    return users

@router.get("/get_all_tokens")
async def get_all_tokens(session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    tokens = session.exec(select(UserTokenModel)).all()
    return tokens
    
@router.get("/me")
async def about_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_data = decode_access_token(token)
    return {"user_data": user_data}
    
# @router.get("/user-email-tokens")
# async def about_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
#     try:
#         user_data = decode_access_token(token)
#         user_email = user_data.get("sub").get("email")
#         # user = session.get(UserModel, user_id)
#         user = session.execute(select(UserModel).where(UserModel.email==user_email)).first()
#         return {"user": user, "user_data": user_data}
#     except Exception as e:
#         return {"error": str(e)}

