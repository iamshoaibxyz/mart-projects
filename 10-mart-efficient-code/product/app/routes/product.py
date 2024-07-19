from uuid import UUID
from app.config.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.schemas.product import ProductAddReq, ProductUpdateReq, ProductAddWithInventoryReq, ProductGetByIdReq, ProductsGetByCompanyIdReq, ProductModelSchema, ProductsGetByProductAndCompanyIdReq
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.database import get_session
from app.models.product import ProductModel
from app.services.kafka.producer import get_producer
from app.schemas.protos import customs_pb2
from sqlmodel import Session
from typing import Annotated
from sqlmodel import select
from app.utils.proto_conversion import product_to_proto
from app.utils.check_auth import auth_checker

router = APIRouter(prefix="/product", tags=["Product"], responses={404: {"description": "Not found"}})

oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/company/company-login")

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]

@router.post("/add-product", status_code=status.HTTP_201_CREATED)
async def add_product(product_data:ProductAddReq, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
    company = await auth_checker(token=token)
    if product_data.category not in categories:
        raise HTTPException(status_code=402, detail=f"Add a specific category keyword like {categories}, {product_data}")
    product = ProductModel(name=product_data.name, category=product_data.category, description=product_data.description, price=product_data.price, company_id=UUID(company.get("id")) )
    
    proto_product = product_to_proto(product)    
    async with get_producer() as producer:
        await producer.send_and_wait("product-added", proto_product.SerializeToString())
    return { "company": company, "product": product, "status": status.HTTP_201_CREATED, "message": "you have succcessfully added the product and we have send you an email for confirmation"}
 
# @router.post("/add-product-with-inventory", status_code=status.HTTP_201_CREATED)
# async def add_product_with_inventory(product_data:ProductAddWithInventoryReq, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
#     company = auth_checker(session=session, token=token)
#     proto_product = customs_pb2.ProductWithInventory(name=product_data.name, description=product_data.description, category=product_data.category, price=float(product_data.price), stock=int(product_data.stock), company_id=str(company.id))
#     async with get_producer() as producer:
#         await producer.send_and_wait("product-product-product-and-inventory-added", proto_product.SerializeToString())
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

@router.get("/get-product-by-id/{product_id}", response_model=ProductModelSchema)
async def product_by_company_(product_id: str, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    product = session.exec(select(ProductModel).where(ProductModel.id==UUID(product_id))).first()
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

@router.post("/get-product-by-product-and-company-id")
async def product_by_company_id(ids: ProductsGetByProductAndCompanyIdReq, session: Annotated[Session, Depends(get_session)]): #, token: Annotated[str, Depends(oauth2_company_scheme)]): #, producer: Annotated[AIOKafkaProducer, Depends(get_producer)]
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id==UUID(ids.company_id), ProductModel.id==UUID(ids.product_id))).first()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"company's product not Found")    
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
 
# @router.put("/update-product")
# async def update_product(product_id: str, product_updated_data: ProductUpdateReq, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
#     company = auth_checker(session=session, token=token)
#     product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id==UUID(product_id), ProductModel.company_id==company.id )).first()
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
#     updated_product = product_updated_data.model_dump(exclude_unset=True)
#     product.sqlmodel_update(updated_product)
#     product.company = company
#     async with get_producer() as producer:
#         product_proto = product_to_proto(product)
#         await producer.send_and_wait("product_product_product_updated", product_proto.SerializeToString())
#     return { "messages": "product updated successfully", "company": company, "updated_product": updated_product, "product":product }
 