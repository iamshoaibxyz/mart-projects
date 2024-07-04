from uuid import UUID
from app.config.security import hashed_password, verify_hashed_password, hashed_url, verify_hashed_url, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.company import CompanyReq, VerifyCompanyReq, CompanyToken, CompanyTokenReq
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.validation import validate_password
from datetime import datetime, timedelta, timezone
from app.config.database import get_session
from app.models.all_models import CompanyModel, CompanyTokenModel
from app.services.kafka.producer import get_producer
from app.config.settings import TOKEN_EXPIRY
from aiokafka import AIOKafkaProducer
from sqlalchemy.orm import Session
from typing import Annotated, Any
from sqlmodel import select
from app.utils.proto_utils import company_to_proto, company_token_to_proto

router = APIRouter(prefix="/company", tags=["Company Auth"], responses={404: {"description": "Not found"}})

oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="company/company-login")


@router.post("/register")
async def create_company(company: CompanyReq, session: Annotated[Session, Depends(get_session)]):
    company_name_exist = session.exec(select(CompanyModel).where(CompanyModel.name== company.name.lower())).first()
    company_exist = session.exec(select(CompanyModel).where(CompanyModel.email == company.email)).first()
    if company_exist:
        if company_exist.name==company.name:
            if company_exist.is_verified:
                return {"message": f"Company '{company_exist.name}' is already registered and verified, please visit to login page, and login to your company"}
            # send email to company for verification 
            proto_company = company_to_proto(company_exist)    
            async with get_producer() as producer:
                await producer.send_and_wait("email-to-unverified-company-topic", proto_company.SerializeToString())
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Company '{company_exist.name}' is already registered but not verified, we have send you an email, please check and verify to your company")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"with this email '{company.email}', Company is  already registerd, please use different email to register new company")
    if  company_name_exist:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"with this Company name '{company.name}', Company is already registerd, please use different name")
    
    validate_password(company.password)   
    hash_password = hashed_password(company.password)
    new_company = CompanyModel(name=company.name.lower(), password=str(hash_password), email=company.email.lower(), description=company.description)
    proto_company = company_to_proto(new_company)    
    async with get_producer() as producer:
        await producer.send_and_wait("register-new-company-topic", proto_company.SerializeToString())
    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully signed up the company and we have send you an email, please check and verify"}

@router.post("/verify-company-account")
async def verify_company(company: CompanyTokenReq, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == company.email)).first()
    if not company_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid creadential")
    # if company_exist.is_verified:
    #     return {"message": f"Company '{company_exist.name}' has already verified, please login it"}
    context_str = str(company_exist.get_context_str())
    if not verify_hashed_url(context_str, company.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token eigther is invalid or expired")

    proto_company = company_to_proto(company_exist)    
    async with get_producer() as producer:
        await producer.send_and_wait("verify-new-company-topic", proto_company.SerializeToString())

    return {"status": status.HTTP_201_CREATED, "message": f"This company {company_exist.name} have succcessfully verified, please visit to login"}

@router.post("/company-login")
async def company_login(company: Annotated[Any, Depends(OAuth2PasswordRequestForm)] , session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == company.username.lower())).first()
    if not company_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company with this email '{company.username}'  is not registered here, please visit to signup and register to your company")
    if not verify_hashed_password(company.password, company_exist.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid creadential")
    if not company_exist.is_verified:
        # send company verification email 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company '{company_exist.name}' is not verified, we have send you an email, please check and verify to your company")
    payload = {"id": str(company_exist.id), "name":company_exist.name, "email":company_exist.email}
    token = create_access_token(payload)
    token_expired_at= datetime.now(timezone.utc) + timedelta(minutes=float(TOKEN_EXPIRY))
    company_token = CompanyTokenModel(token=token, expired_at=token_expired_at, company_id=company_exist.id)
    proto_company_token = company_token_to_proto(company_token)
    async with get_producer() as producer:
        await producer.send_and_wait("company-token-topic", proto_company_token.SerializeToString())
        return CompanyToken(access_token=token, token_type="bearer", expires_in=str(token_expired_at)) # {"status": status.HTTP_200_OK, "message": "you have succcessfully login", "token": token, "user": user_exist}

@router.get("/get-all-companies")
async def get_all_companies(session: Annotated[Session, Depends(get_session)], token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    companies = session.exec(select(CompanyModel)).all()
    return companies

# @router.get("/get_all_tokens")
# async def get_all_tokens(session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
#     tokens = session.exec(select(UserTokenModel)).all()
#     return tokens
    
# @router.get("/me")
# async def about_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # user_data = decode_access_token(token)
    # return {"user_data": user_data}


