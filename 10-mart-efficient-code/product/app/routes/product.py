from uuid import UUID
from app.config.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.schemas.product import ProductAddReq, ProductAddWithInventoryReq, ProductGetByIdReq, ProductsGetByCompanyIdReq, ProductModelSchema
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from app.config.database import get_session
from app.models.all_models import ProductModel, CompanyModel, StockLevel, InventoryTransaction
from app.services.kafka.producer import get_producer
from sqlmodel import Session
from typing import Annotated, Any
from sqlmodel import select
from app.utils.proto_utils import product_to_proto

router = APIRouter(prefix="/product", tags=["Product"], responses={404: {"description": "Not found"}})

# oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="company/company-login")

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]

@router.post("/add-product", status_code=status.HTTP_201_CREATED)
async def add_product(product_data:ProductAddReq):
    if product_data.category not in categories:
        raise HTTPException(status_code=402, detail=f"Add a specific category keyword like {categories}, {product_data}")
    product = ProductModel(name=product_data.name, category=product_data.category, description=product_data.description, price=product_data.price, company_id=UUID("f9f6de6c-479a-465f-933a-05c4ae278fe8") )
    
    proto_product = product_to_proto(product)    
    async with get_producer() as producer:
        await producer.send_and_wait("add-new-product-topic", proto_product.SerializeToString())
    return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully added the product and we have send you an email for confirmation"}
 
# @router.post("/add-product-with-inventory", status_code=status.HTTP_201_CREATED)
# async def add_product_with_inventory(product_data:ProductAddWithInventoryReq):
#     product = ProductModel(name=product_data.name, description=product_data.description, price=product_data.price,)
#     # StockLevel, InventoryTransaction
#     proto_product = product_to_proto(product)    
#     async with get_producer() as producer:
#         await producer.send_and_wait("add-new-product-with-inventory-topic", proto_product.SerializeToString())
#     return {"status": status.HTTP_201_CREATED, "message": "you have succcessfully added the product and we have send you an email for confirmation"}
 
@router.get("/get-all-products", response_model=list[ProductModelSchema])
async def all_products(session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    products = session.exec(select(ProductModel)).all()
    return products

@router.post("/get-products-by-price-range", response_model=list[ProductModelSchema])
def products_by_price_range(low_price: float, high_price: float, session: Annotated[Session, Depends(get_session)]):
        results = session.exec(select(ProductModel).where(ProductModel.price.between(float(low_price), float(high_price) )))
        products = results.all()
        return products

@router.get("/get-products-by-low-price", response_model=list[ProductModelSchema])
def products_by_low_price(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(ProductModel).order_by(ProductModel.price.asc()).limit(5)).all()
    return products

@router.get("/get-products-by-high-price", response_model=list[ProductModelSchema])
def products_by_high_price(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(ProductModel).order_by(ProductModel.price.desc()).limit(5)).all()
    return products

@router.post("/get-product-by-id", response_model=ProductModelSchema)
async def product_by_company_(product_id: ProductGetByIdReq, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    product = session.exec(select(ProductModel).where(ProductModel.id==UUID(product_id.id))).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product not Found")    
    return product

@router.post("/get-products-by-company-id", response_model=list[ProductModelSchema])
async def product_by_company_id(company_id: ProductsGetByCompanyIdReq, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id==UUID(company_id.id))).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company's product not Found")    
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company has no product")    
    return company_products

@router.post("/get-company-low-price-product", response_model=list[ProductModelSchema])
async def product_by_company_id(company_id: ProductsGetByCompanyIdReq, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id==UUID(company_id.id)).order_by(ProductModel.price.asc()).limit(5)).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company's product not Found")    
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company has no product")    
    return company_products

@router.post("/get-company-high-price-product", response_model=list[ProductModelSchema])
async def product_by_company_id(company_id: ProductsGetByCompanyIdReq, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id==UUID(company_id.id)).order_by(ProductModel.price.desc()).limit(5)).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company's product not Found")    
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company has no product")    
    return company_products




































# @router.get("/company-token")
# async def about_company(token: Annotated[str, Depends(oauth2_company_scheme)]):
#     try:
#         company_data = decode_access_token(token)
#         detail = company_data.get("sub").get("id")
#         return {"company_data": company_data, "detail": detail}
#     except Exception as e:
#         return {"error": str(e)}

# @router.get("/company-profile", response_model=CompanySchema)
# async def about_company(token: Annotated[str, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
#     try:
#         company_data = decode_access_token(token)
#         id = company_data.get("sub").get("id")
#         company = session.get(CompanyModel, UUID(id))
#         return company
#     except Exception as e:
#         return {"error": str(e)}

# @router.get("/get-company-by-id/{id}", response_model=CompanyBasicInfoRes)
# async def company_by_id(data: getCompanyByIdReq, session: Annotated[Session, Depends(get_session)]):
#     company = session.exec(select(CompanyModel).where(CompanyModel.id==UUID(data.id))).first()
#     if not company:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company not Found")    
#     return company

# @router.put("/update-profile")
# async def update_profile(updated_data: UpdateCompanyProfileReq, token: Annotated[str, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
#     try:
#         decoded_token = decode_access_token(token)
#         company_id = decoded_token.get("sub").get("id")        
#         company = session.get(CompanyModel, UUID(company_id))
#         if not company:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
#         # Check if the new company name already exists
#         if updated_data.name:
#             company_name_exist = session.exec(select(CompanyModel).where(CompanyModel.name == updated_data.name.lower())).first()
#             if company_name_exist and company_name_exist.name != company.name:
#                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company name {updated_data.name} is already used")
        
#         # Check if the new company email already exists
#         if updated_data.email:
#             company_email_exist = session.exec(select(CompanyModel).where(CompanyModel.email == updated_data.email.lower())).first()
#             if company_email_exist and company_email_exist.email != company.email:
#                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Company email {updated_data.email} is already used")
        
#         # Update the company details
#         for key, value in updated_data.model_dump(exclude_unset=True).items():
#             setattr(company, key, value)
#         company.updated_at = datetime.now(timezone.utc)
#         proto_company = company_to_proto(company)    
#         async with get_producer() as producer:
#             await producer.send_and_wait("update-company-topic", proto_company.SerializeToString())
                
#         return {"msg": "Profile updated successfully"}
    
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
