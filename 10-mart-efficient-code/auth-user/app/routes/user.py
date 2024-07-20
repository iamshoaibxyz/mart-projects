from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from typing import Annotated, Any
from pydantic import EmailStr
from sqlmodel import select
from uuid import UUID

from app.schemas.user import UserReq, UserAccountVerifyReq, UserToken, VerifyResetPasswordUserReq, UserBasicInfoRes, GetUserByEmailReq, GetUserByIdReq, UpdataUserProfileReq 
from app.config.security import hashed_password, hashed_url, verify_hashed_password , verify_hashed_url, create_access_token, decode_access_token
from app.utils.proto_conversion import user_to_proto, user_token_to_proto
from app.models.user import UserModel, UserTokenModel
from app.services.kafka.producer import get_producer
from app.config.validation import validate_password
from app.config.settings import TOKEN_EXPIRY
from app.config.database import get_session

router = APIRouter(prefix="/user", tags=["User Auth"], responses={404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/user-login")

from app.schemas.user import UserSchema
 
@router.post("/register")
async def create_user(user: UserReq, session: Annotated[Session, Depends(get_session)]):
    if not user.email.endswith("@gmail.com"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Gmail addresses are allowed")
    user_exist = session.exec(select(UserModel).where(UserModel.email == user.email)).first()
    if user_exist:
        if user_exist.is_verified:
            return {"message": f"user '{user.email}' email is already registed and verified, please visit to login"}
        # Send email to user for verification
        proto_user = user_to_proto(user_exist)    
        async with get_producer() as producer:
            await producer.send_and_wait("email-verification-to-unverified-user", proto_user.SerializeToString())
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user '{user.email}' is already exists, but not verified, we have sent you an email, please check and verify")
    validate_password(user.password)
    hash_password = hashed_password(user.password)
    new_user = UserModel(first_name=user.first_name.lower(), last_name=user.last_name.lower(), password=str(hash_password), email=user.email.lower())
    proto_user = user_to_proto(new_user)    
    async with get_producer() as producer:
        await producer.send_and_wait("user-added", proto_user.SerializeToString())
    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully signed up and we have send you an email, please check and verify"}

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
        await producer.send_and_wait("user-verify-updated", proto_user.SerializeToString())

    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully verified, please visit to login"}

@router.post("/user-login", response_model=UserToken)
async def user_login(user: Annotated[Any, Depends(OAuth2PasswordRequestForm)] , session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user_exist: UserModel = session.exec(select(UserModel).where(UserModel.email == user.username.lower())).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user '{user.username}' is not registered, please visit to signup and register to yourself")
    if not verify_hashed_password(user.password, user_exist.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid creadential")
    if not user_exist.is_verified:
        # send user verification email
        proto_user = user_to_proto(user_exist)    
        async with get_producer() as producer:
            await producer.send_and_wait("email-verification-to-unverified-user", proto_user.SerializeToString())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user '{user.username}' is not verified, we have send you and email, please check and verify to yourself")
    payload = {"id": str(user_exist.id), "first_name":user_exist.first_name, "last_name":user_exist.last_name, "email":user_exist.email}
    token = create_access_token(payload)
    token_expired_at= datetime.now(timezone.utc) + timedelta(minutes=float(TOKEN_EXPIRY))
    user_token = UserTokenModel(token=token, expired_at=token_expired_at, user_id=user_exist.id)
    proto_user_token = user_token_to_proto(user_token)
    async with get_producer() as producer:
        await producer.send_and_wait("user-token-added", proto_user_token.SerializeToString())
    return UserToken(access_token=token, token_type="bearer", expires_in=str(token_expired_at)) # {"status": status.HTTP_200_OK, "message": "you have succcessfully login", "token": token, "user": user_exist}

@router.post("/reset-password-request")
async def reset_user_password(email: EmailStr, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user_exist: UserModel = session.exec(select(UserModel).where(UserModel.email == email.lower())).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user email '{email}' is not registered, please visit to signup and register to yourself")
    if not user_exist.is_verified:
        proto_user = user_to_proto(user_exist)    
        async with get_producer() as producer:
            await producer.send_and_wait("email-verification-to-unverified-user", proto_user.SerializeToString())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user email '{email}' is not verified, first verified and then you can change the password, please check and verify the email")
    proto_user = user_to_proto(user_exist)
    async with get_producer() as producer:
        await producer.send_and_wait("email-user-reset-password", proto_user.SerializeToString())
    return {"status": status.HTTP_200_OK, "message": f"Email has been sent to {email}, please check and verify"}
 
@router.post("/verify-reset")
async def verify_reset_user_password(user_data: VerifyResetPasswordUserReq, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user_exist: UserModel = session.exec(select(UserModel).where(UserModel.email == user_data.email.lower())).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user email '{user_data.email}' is not Found")
    verification_context = str(user_exist.get_context_str())
    if not verify_hashed_url(db_url=verification_context, user_url=user_data.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user token eighter is expired or invalid")
    validate_password(user_data.new_password)
    new_password = hashed_password(user_data.new_password)
    user_exist.password = new_password
    user_exist.updated_at = datetime.now(timezone.utc)
    proto_user = user_to_proto(user_exist)    
    async with get_producer() as producer:
        await producer.send_and_wait("user-password-updated", proto_user.SerializeToString())
    return {"status": status.HTTP_200_OK, "message": f"Password successfully has been changed"}

@router.get("/get_all_users", response_model=list[UserBasicInfoRes])
async def get_all_users(session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    users = session.exec(select(UserModel)).all()
    return users

@router.get("/get_user_by_id/{user_id}", response_model=UserBasicInfoRes)
async def get_all_users(user_id: UUID, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    user = session.exec(select(UserModel).where(UserModel.id==user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user not Found")    
    return user

@router.get("/get-user-by-email/{email}", response_model=UserBasicInfoRes)
async def user_by_email(email: EmailStr, session: Annotated[Session, Depends(get_session)]):
    user = session.exec(select(UserModel).where(UserModel.email==email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user not Found")    
    return user

@router.get("/user-token")
async def about_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    user_data = decode_access_token(token)
    return user_data

@router.get("/user-profile")
async def about_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        user_data = decode_access_token(token)
        id = user_data.get("sub").get("id")
        user = session.get(UserModel, UUID(id))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return user
    except Exception as e:
        return {"error": str(e)}

@router.delete("/delete-user")
async def delete_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        user_data = decode_access_token(token)
        id = user_data.get("sub").get("id")
        user = session.get(UserModel, UUID(id))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        proto_user = user_to_proto(user)    
        async with get_producer() as producer:
            await producer.send_and_wait("user-deleted", proto_user.SerializeToString())
                
        return {"message": "user has successfully deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  