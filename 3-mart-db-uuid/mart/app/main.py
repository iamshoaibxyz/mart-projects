from fastapi import FastAPI, HTTPException, Depends
from app import setting
from app.schema import Product, ProductReq, UpdateProduct, OrderPlace, Order
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

connection_str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating table")
    SQLModel.metadata.create_all(engine)
    print("table created")
    yield

app: FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def root():
    return {"Message":"Mart API Sourcecode"}

@app.get("/get-all-products", response_model=list[Product])
def all_products(session: Annotated[Session, Depends(get_session) ] ):
    products = session.exec(select(Product)).all()
    print(products)
    return products

@app.get("/get-products-by-cotegory/${product_category}", response_model=list[Product])
def products_by_category(product_category: str, session: Annotated[Session, Depends(get_session) ] ):
    if product_category not in categories:
        raise HTTPException(status_code=402, detail="write a valiad keyword")
    products = session.exec(select(Product).where(Product.category==product_category)).all()
    return products

@app.get("/get-product/${product_id}", response_model=Product)
def get_product(product_id: UUID, session: Annotated[Session, Depends(get_session) ] ):
    product = session.exec(select(Product).where(Product.id==product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@app.post("/add-product", response_model=Product)
def add_product(product: ProductReq, session: Annotated[Session, Depends(get_session) ] ):
    if product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")
    ready_product = Product(name=product.name, price=product.price, category=product.category, quantity=product.quantity)
    print(ready_product)
    session.add(ready_product)
    session.commit()
    session.refresh(ready_product)
    return ready_product

@app.patch("/increment_product_item/${product_id}", response_model=Product)
def update_product_item(product_id: UUID, add_item: int, session: Annotated[Session, Depends(get_session) ] ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    db_product.quantity += int(add_item)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.patch("/update_product/${product_id}", response_model=Product)
def update_product(product_id: UUID, product: UpdateProduct, session: Annotated[Session, Depends(get_session) ] ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    updated_product = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(updated_product) 
    if db_product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
 
@app.post("/order/", response_model=OrderPlace)
def order_place(order:Order, session: Annotated[Session, Depends(get_session)]):
    print(order)
    product: Product | None = session.exec(select(Product).where(Product.id==order.product_id)).first()
    print(product)
    if not product:
        raise HTTPException(status_code=402, detail="product does not exist")
    if product.quantity < int(order.quantity):
        raise HTTPException(status_code=402, detail=f"Sorry, we have only {product.quantity} item of {product.name}")
    
    new_order = OrderPlace(product_id=order.product_id, quantity=order.quantity, product_price=product.price, product_name=product.name, product_category=product.category, totle_price=(product.price * order.quantity) )
    product.quantity -= order.quantity  # update product detait(quantity)

    session.add(product)
    session.add(new_order)
    session.commit()
    session.refresh(product)
    session.refresh(new_order)
    return new_order

@app.get("/get_orders", response_model=list[OrderPlace])
def get_orders( session: Annotated[Session, Depends(get_session)]):
    orders = session.exec(select(OrderPlace)).all()
    return orders
