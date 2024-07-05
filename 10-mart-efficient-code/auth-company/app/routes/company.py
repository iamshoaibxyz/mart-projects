from uuid import UUID

from pydantic import EmailStr
from app.config.security import hashed_password, verify_hashed_password, verify_hashed_url, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.company import UpdateCompanyProfileReq, CompanyReq, CompanyToken, CompanyTokenReq, CompanySchema, VerifyResetPasswordCompanyReq
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.config.validation import validate_password
from datetime import datetime, timedelta, timezone
from app.config.database import get_session
from app.models.all_models import CompanyModel, CompanyTokenModel
from app.services.kafka.producer import get_producer
from app.config.settings import TOKEN_EXPIRY
from sqlalchemy.orm import Session
from typing import Annotated, Any
from sqlmodel import select
from app.utils.proto_utils import company_to_proto, company_token_to_proto

router = APIRouter(prefix="/company", tags=["Company Auth"], responses={404: {"description": "Not found"}})

oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="company/company-login")

@router.post("/register")
async def create_company(company: CompanyReq, session: Annotated[Session, Depends(get_session)]):
    company_name_exist = session.exec(select(CompanyModel).where(CompanyModel.name== company.name.lower())).first()
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == company.email.lower())).first()
    if company_exist:
        if company_exist.name==company.name.lower():
            if company_exist.is_verified:
                return {"message": f"Company '{company_exist.name}' is already registered and verified, please visit to login page, and login to your company"}
            # send email to company for verification 
            proto_company1 = company_to_proto(company_exist)    
            async with get_producer() as producer:
                await producer.send_and_wait("email-to-unverified-company-topic", proto_company1.SerializeToString())
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Company '{company_exist.name}' is already registered but not verified, we have send you an email, please check and verify to your company")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"with this email '{company.email}', Company is  already registerd, please use different email to register new company")
    if  company_name_exist:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"with this Company name '{company.name}', Company is already registerd, please use different name")
    
    validate_password(company.password)   
    hash_password = hashed_password(company.password)
    new_company = CompanyModel(name=company.name.lower(), password=str(hash_password), email=company.email.lower(), description=company.description)
    proto_company2 = company_to_proto(new_company)    
    async with get_producer() as producer:
        await producer.send_and_wait("register-new-company-topic", proto_company2.SerializeToString())
    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully signed up the company and we have send you an email, please check and verify"}

@router.post("/verify-company-account")
async def verify_company(company: CompanyTokenReq, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == company.email.lower())).first()
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
        proto_company = company_to_proto(company_exist)    
        async with get_producer() as producer:
            await producer.send_and_wait("email-to-unverified-company-topic", proto_company.SerializeToString())             
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company '{company_exist.name}' is not verified, we have send you an email, please check and verify to your company")
    payload = {"id": str(company_exist.id), "name":company_exist.name, "email":company_exist.email}
    token = create_access_token(payload)
    token_expired_at= datetime.now(timezone.utc) + timedelta(minutes=float(TOKEN_EXPIRY))
    company_token = CompanyTokenModel(token=token, expired_at=token_expired_at, company_id=company_exist.id)
    proto_company_token = company_token_to_proto(company_token)
    async with get_producer() as producer:
        await producer.send_and_wait("company-token-topic", proto_company_token.SerializeToString())
    return CompanyToken(access_token=token, token_type="bearer", expires_in=str(token_expired_at)) # {"status": status.HTTP_200_OK, "message": "you have succcessfully login", "token": token, "user": user_exist}

@router.post("/reset-password-request")
async def reset_company_password(email: EmailStr, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == email.lower())).first()
    if not company_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company email '{email}' is not registered, please visit to signup and register to the company")
    proto_company = company_to_proto(company_exist)    
    async with get_producer() as producer:
        await producer.send_and_wait("email-to-reset-password-company-topic", proto_company.SerializeToString())
    return {"status": status.HTTP_200_OK, "message": f"Email has been sent to {email}, please check and set new password"}

@router.post("/verify-reset")
async def verify_reset_user_password(company_data: VerifyResetPasswordCompanyReq, session: Annotated[Session, Depends(get_session)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_exist: CompanyModel = session.exec(select(CompanyModel).where(CompanyModel.email == company_data.email.lower())).first()
    if not company_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company email '{company_data.email}' is not Found")
    verification_context = str(company_exist.get_context_str("VERIFY_COMPANY_CONTEXT"))
    if not verify_hashed_url(db_url=verification_context, user_url=company_data.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="company token eighter is expired or invalid")
    validate_password(company_data.new_password)
    new_password = hashed_password(company_data.new_password)
    company_exist.password = new_password
    company_exist.updated_at = datetime.now(timezone.utc)
    proto_company = company_to_proto(company_exist)    
    async with get_producer() as producer:
        await producer.send_and_wait("verify-reset-password-company-topic", proto_company.SerializeToString())
    return {"status": status.HTTP_200_OK, "message": f"Password successfully has been changed"}

@router.post("/logout")
async def logout(response: Response):
    response.headers["Authorization"] = ""
    return {"msg": "Logged out successfully"}

@router.get("/get-all-companies")
async def get_all_companies(session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    companies = session.exec(select(CompanyModel)).all()
    return companies

@router.get("/company-token")
async def about_company(token: Annotated[str, Depends(oauth2_company_scheme)]):
    try:
        company_data = decode_access_token(token)
        detail = company_data.get("sub").get("id")
        return {"company_data": company_data, "detail": detail}
    except Exception as e:
        return {"error": str(e)}

@router.get("/company-profile", response_model=CompanySchema)
async def about_company(token: Annotated[str, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        company_data = decode_access_token(token)
        id = company_data.get("sub").get("id")
        company = session.get(CompanyModel, UUID(id))
        return company
    except Exception as e:
        return {"error": str(e)}

@router.put("/update-profile")
async def update_profile(updated_data: UpdateCompanyProfileReq, token: Annotated[str, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        decoded_token = decode_access_token(token)
        company_id = decoded_token.get("sub").get("id")        
        company = session.get(CompanyModel, UUID(company_id))
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        # Check if the new company name already exists
        if updated_data.name:
            company_name_exist = session.exec(select(CompanyModel).where(CompanyModel.name == updated_data.name.lower())).first()
            if company_name_exist and company_name_exist.name != company.name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company name {updated_data.name} is already used")
        
        # Check if the new company email already exists
        if updated_data.email:
            company_email_exist = session.exec(select(CompanyModel).where(CompanyModel.email == updated_data.email.lower())).first()
            if company_email_exist and company_email_exist.email != company.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company email {updated_data.email} is already used")
        
        # Update the company details
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        company.updated_at = datetime.now(timezone.utc)
        proto_company = company_to_proto(company)    
        async with get_producer() as producer:
            await producer.send_and_wait("update-company-topic", proto_company.SerializeToString())
                
        return {"msg": "Profile updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
