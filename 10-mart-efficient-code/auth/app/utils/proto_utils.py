from datetime import datetime
from uuid import UUID
from app.schemas.protobuf import user_pb2, user_token_pb2, company_pb2, company_token_pb2
from app.models.all_models import CompanyModel, CompanyTokenModel, UserModel, UserTokenModel

def user_to_proto(user: UserModel) -> user_pb2.User:
    user_proto = user_pb2.User(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email,
        is_verified=user.is_verified,
        verified_at=user.verified_at.isoformat() if user.verified_at else "",
        updated_at=user.updated_at.isoformat() if user.updated_at else "",
        created_at=user.created_at.isoformat()
    )
    return user_proto

def proto_to_userdict(user_proto: user_pb2.User) -> dict:
    user_dict = {
        "id": UUID(user_proto.id),
        "first_name": user_proto.first_name,
        "last_name": user_proto.last_name,
        "password": user_proto.password,
        "email": user_proto.email,
        "is_verified": user_proto.is_verified,
        "verified_at": datetime.fromisoformat(user_proto.verified_at) if user_proto.verified_at else None,
        "updated_at": datetime.fromisoformat(user_proto.updated_at) if user_proto.updated_at else None,
        "created_at": datetime.fromisoformat(user_proto.created_at)
    }
    return user_dict

def proto_to_usermodel(user_proto: user_pb2.User) -> UserModel:
    user = UserModel(
        id=UUID(user_proto.id),
        first_name=user_proto.first_name,
        last_name=user_proto.last_name,
        password=user_proto.password,
        email=user_proto.email,
        is_verified=user_proto.is_verified,
        verified_at=datetime.fromisoformat(user_proto.verified_at) if user_proto.verified_at else None,
        updated_at=datetime.fromisoformat(user_proto.updated_at) if user_proto.updated_at else None,
        created_at=datetime.fromisoformat(user_proto.created_at)
    )
    return user

def user_token_to_proto(user_token: UserTokenModel) -> user_token_pb2.UserToken:
    return user_token_pb2.UserToken(
        id=str(user_token.id),
        user_id=str(user_token.user_id),
        token=user_token.token,
        created_at=user_token.created_at.isoformat(),
        expired_at=user_token.expired_at.isoformat(),
    )

def proto_to_user_token(proto_user_token: user_token_pb2.UserToken) -> UserTokenModel:
    return UserTokenModel(
        id=UUID(proto_user_token.id),
        token=proto_user_token.token,
        user_id=UUID(proto_user_token.user_id),
        created_at=datetime.fromisoformat(proto_user_token.created_at),
        expired_at=datetime.fromisoformat(proto_user_token.expired_at),
    )

def company_to_proto(company: CompanyModel) -> company_pb2.Company:
    return company_pb2.Company(
        id=str(company.id),
        name=company.name,
        description=company.description if company.description else "",
        email=company.email,
        password=company.password,
        is_verified=company.is_verified,
        verified_at=company.verified_at.isoformat() if company.verified_at else "",
        created_at=company.created_at.isoformat(),
        updated_at=company.updated_at.isoformat() if company.updated_at else "",
    )

def proto_to_company(proto_company: company_pb2.Company) -> CompanyModel:
    return CompanyModel(
        id=UUID(proto_company.id),
        name=proto_company.name,
        description=proto_company.description if proto_company.description else None,
        email=proto_company.email,
        password=proto_company.password,
        is_verified=proto_company.is_verified,
        verified_at=datetime.fromisoformat(proto_company.verified_at) if proto_company.verified_at else None,
        created_at=datetime.fromisoformat(proto_company.created_at),
        updated_at=datetime.fromisoformat(proto_company.updated_at) if proto_company.updated_at else None,
    )

def company_token_to_proto(company_token: CompanyTokenModel) -> company_token_pb2.CompanyToken:
    return company_token_pb2.CompanyToken(
        id=str(company_token.id),
        company_id=str(company_token.company_id),
        token=company_token.token,
        created_at=company_token.created_at.isoformat(),
        expired_at=company_token.expired_at.isoformat(),
    )

def proto_to_company_token(proto_company_token: company_token_pb2.CompanyToken) -> CompanyTokenModel:
    return CompanyTokenModel(
        id=UUID(proto_company_token.id),
        company_id=UUID(proto_company_token.company_id),
        token=proto_company_token.token,
        created_at=datetime.fromisoformat(proto_company_token.created_at),
        expired_at=datetime.fromisoformat(proto_company_token.expired_at),
    )