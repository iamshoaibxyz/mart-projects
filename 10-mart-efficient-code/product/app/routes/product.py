from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from app.schemas.product import ProductAddReq, ProductAddWithInventoryReq, ProductModelSchema, ProductUpdateReq
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
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

categories = ["food", "health", "fashion", "electronics", "sports", "vehicle", "furniture", "literature", "other"]

@router.post("/add-product", status_code=status.HTTP_201_CREATED, description="Add a new product")
async def add_product( product_data: ProductAddReq, token: Annotated[dict, Depends(oauth2_company_scheme)] ):
    """
    Add a new product to the company's inventory.
    
    - **product_data**: The product data.
    - **token**: The authentication token.
    """
    company = await auth_checker(token=token)
    if product_data.category not in categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Add a specific category keyword like {categories}")
    if product_data.price < 5 or product_data.price > 50000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"price bust be greather than 5, less then 50k")
    product = ProductModel(name=product_data.name, category=product_data.category, description=product_data.description, price=product_data.price, company_id=UUID(company.get("id")) )
    
    proto_product = product_to_proto(product)
    async with get_producer() as producer:
        await producer.send_and_wait("product-added", proto_product.SerializeToString())
    return { "status": status.HTTP_201_CREATED, "message": "You have successfully added the product and we have sent you an email for confirmation"}

@router.post("/add-product-with-inventory", status_code=status.HTTP_201_CREATED, description="Add a new product along with inventory details")
async def add_product_with_inventory( product_data: ProductAddWithInventoryReq, token: Annotated[dict, Depends(oauth2_company_scheme)] ):
    """
    Add a new product along with its inventory details.
    
    - **product_data**: The product and inventory data.
    - **token**: The authentication token.
    """
    company = await auth_checker(token=token)
    if product_data.category not in categories:
        raise HTTPException(status_code=402, detail=f"Add a specific category keyword like {categories}")
    if product_data.price < 5 or product_data.price > 50000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"price must be greather than 5, less then 1k")
    if product_data.stock < 5 or product_data.stock > 1000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"stock must be greather than 5, less then 1k")
    proto_product = customs_pb2.ProductWithInventory(name=product_data.name, description=product_data.description, category=product_data.category, price=float(product_data.price), stock=int(product_data.stock), company_id=str(company.get("id")))
    async with get_producer() as producer:
        await producer.send_and_wait("product-and-inventory-added", proto_product.SerializeToString())
    return {"status": status.HTTP_201_CREATED, "message": "You have successfully added the product and inventory. We will send you an email for confirmation"}

@router.get("/get-all-products", response_model=list[ProductModelSchema], description="Retrieve all products")
async def all_products(session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve all products.
    
    - **session**: The database session.
    """
    products = session.exec(select(ProductModel)).all()
    return products

@router.get("/get-products-by-price-range", response_model=list[ProductModelSchema], description="Retrieve products within a specific price range")
def products_by_price_range(session: Annotated[Session, Depends(get_session)], low_price: Annotated[float, Query(..., lt=1000, gt=5, description="The lower bound of the price range")], high_price: Annotated[float, Query(..., lt=50000, gt=999, description="The upper bound of the price range")] ):
    """
    Retrieve products within a specific price range.
    
    - **low_price**: The lower bound of the price range.
    - **high_price**: The upper bound of the price range.
    - **session**: The database session.
    """
    results = session.exec(select(ProductModel).where(ProductModel.price.between(float(low_price), float(high_price))))
    products = results.all()
    return products

@router.get("/get-products-by-low-price", response_model=list[ProductModelSchema], description="Retrieve top 5 products with the lowest prices")
def products_by_low_price(session: Annotated[Session, Depends(get_session)]):
    """
    Retrieve the top 5 products with the lowest prices.
    
    - **session**: The database session.
    """
    products = session.exec(select(ProductModel).order_by(ProductModel.price.asc()).limit(5)).all()
    return products

@router.get("/get-products-by-high-price", response_model=list[ProductModelSchema], description="Retrieve top 5 products with the highest prices")
def products_by_high_price(session: Annotated[Session, Depends(get_session)]):
    """
    Retrieve the top 5 products with the highest prices.
    
    - **session**: The database session.
    """
    products = session.exec(select(ProductModel).order_by(ProductModel.price.desc()).limit(5)).all()
    return products

@router.get("/get-product-by-id/{product_id}", response_model=ProductModelSchema, description="Retrieve a product by its ID")
async def product_by_id(product_id: Annotated[UUID, Path(..., description="The ID of the product")], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve a product by its ID.
    
    - **product_id**: The ID of the product.
    - **session**: The database session.
    """
    product = session.exec(select(ProductModel).where(ProductModel.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")
    return product

@router.get("/get-products-by-company-id/{company_id}", response_model=list[ProductModelSchema], description="Retrieve all products of a company by the company's ID")
async def product_by_company_id(company_id: Annotated[UUID, Path(..., description="The ID of the company")], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve all products of a company by the company's ID.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    """
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id == company_id)).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company has no products")
    return company_products

@router.get("/get-product-by-product-and-company-id", response_model=ProductModelSchema, description="Retrieve a product by its ID and company's ID")
async def product_by_product_and_company_id( session: Annotated[Session, Depends(get_session)], company_id: UUID = Query(description="The ID of the company"), product_id: UUID = Query(description="The ID of the product"), ): 
    """
    Retrieve a product by its ID and company's ID.
    
    - **company_id**: The ID of the company.
    - **product_id**: The ID of the product.
    - **session**: The database session.
    """
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id == company_id, ProductModel.id == product_id)).first()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    return company_products

@router.get("/get-company-low-price-product/{company_id}", response_model=list[ProductModelSchema], description="Retrieve the top 5 lowest priced products of a company")
async def low_price_product_by_company_id(company_id: Annotated[UUID, Path(..., description="The ID of the company")], session: Annotated[Session, Depends(get_session)]):
    """
    Retrieve the top 5 lowest priced products of a company.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    """
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id == company_id).order_by(ProductModel.price.asc()).limit(5)).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company has no products")
    return company_products

@router.get("/get-company-high-price-product/{company_id}", response_model=list[ProductModelSchema], description="Retrieve the top 5 highest priced products of a company")
async def high_price_product_by_company_id(company_id: Annotated[UUID, Path(..., description="The ID of the company")], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve the top 5 highest priced products of a company.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    """
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id == company_id).order_by(ProductModel.price.desc()).limit(5)).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company has no products")
    return company_products

@router.get("/get-current-company-products/", response_model=list[ProductModelSchema], description="Retrieve all products of a company by the company's ID")
async def current_company_products(token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve all products of a company by the company's ID.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    - **token**: The authentication token.
    """
    company = await auth_checker(token=token)
    company_products = session.exec(select(ProductModel).where(ProductModel.company_id == UUID(company.get("id")))).all()
    if not company_products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    if not len(company_products) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company has no products")
    return company_products

@router.get("/get-company-product-by-id/{product_id}", description="Retrieve all products of a company by the company's ID")
async def current_company_product_by_product_id(product_id: UUID, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve all products of a company by the company's ID.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    - **token**: The authentication token.
    """
    company = await auth_checker(token=token)
    company_product = session.exec(select(ProductModel).where( ProductModel.id==product_id, ProductModel.company_id == UUID(company.get("id")))).first()
    if not company_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    return company_product

@router.delete("/delete-company-products/{product_id}", description="Retrieve all products of a company by the company's ID")
async def delete_current_company_product_by_product_id(product_id: UUID, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]): 
    """
    Retrieve all products of a company by the company's ID.
    
    - **company_id**: The ID of the company.
    - **session**: The database session.
    - **token**: The authentication token.
    """
    company = await auth_checker(token=token)
    company_product = session.exec(select(ProductModel).where( ProductModel.id==product_id, ProductModel.company_id == UUID(company.get("id")))).first()
    if not company_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company's product not found")
    session.delete(company_product)
    session.commit()
    return {"message": "company product successfully deleted"}


@router.put("/update-product/{product_id}")
async def update_current_company_product(product_id: UUID, product_updated_data: ProductUpdateReq, token: Annotated[dict, Depends(oauth2_company_scheme)], session: Annotated[Session, Depends(get_session)]):
    company = await auth_checker(token=token)
    product: ProductModel = session.exec(select(ProductModel).where(ProductModel.id==product_id, ProductModel.company_id== UUID(company.get("id")) )).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    updated_product = product_updated_data.model_dump(exclude_unset=True)
    product.sqlmodel_update(updated_product)
    if product.category not in categories:
        raise HTTPException(status_code=402, detail=f"Add a specific category keyword like {categories}")
    if product.price < 5 or product.price > 50000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"price must be greather than 5, less then 1k")
    async with get_producer() as producer:
        product_proto = product_to_proto(product)
        await producer.send_and_wait("product_updated", product_proto.SerializeToString())
    return { "messages": "product updated successfully", "company": company, "updated_product": updated_product, "product":product }
 