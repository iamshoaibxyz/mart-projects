

from fastapi import FastAPI, HTTPException, Depends
from app import setting
from app.schema import Product, ProductReq, UpdateProduct, OrderPlace, Order
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
# logging.basicConfig(level=logging.DEBUG)

connection_str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

def get_session():
    with Session(engine) as session:
        yield session

async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def kafka_consumer(topic:str, bootstrap_server:str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_server, group_id="mart_group" ,auto_offset_reset="earliest")
    await consumer.start()
    try:  
        
        if topic=="mart-product-topic":
            async for message in consumer:
                data_dict = json.loads(message.value)
                id = UUID(data_dict.pop("id")) # Extract the id from the dictionary and change str datatype to UUID
                # Initialize the Product instance using the extracted id
                product_instance = Product(id=id, **data_dict) # if dont pass `id` it will generate new id, here we dont need to new id because we generated before in `add-product` route
                with Session(engine) as session:               
                    session.add(product_instance)
                    session.commit()

        elif topic=="mart-order-topic":
            async for message in consumer:
                data_dict = json.loads(message.value) # Parse JSON data into a Python dictionary
                order_id = UUID(data_dict.pop("order_id")) # Extract the id from the dictionary
                product_id = UUID(data_dict.pop("product_id"))

                # Initialize the Product instance using the extracted id
                Order_instance = OrderPlace(order_id=order_id, product_id=product_id, **data_dict) 
                with Session(engine) as session:   
                    session.add(Order_instance)
                    session.commit()

        elif topic=="mart-product-decrease-topic":
            async for message in consumer:
                data_dict = json.loads(message.value)
                order_id = UUID(data_dict.pop("order_id"))
                product_id = UUID(data_dict.pop("product_id"))
                product_instance = OrderPlace(order_id=order_id,product_id=product_id, **data_dict) 
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, product_instance.product_id)
                    product.quantity -= product_instance.quantity 
                    session.add(product)
                    session.commit()

        elif topic=="mart-update-product-topic":
            async for message in consumer:
                dict_data = json.loads(message.value)   # json to dict
                updated_product = dict_data.pop("updated_product")  # Extract recived value("updated_product") from dict 
                db_product_id = dict_data.pop("db_product_id")      # Extract recived value("db_product_id") from dict 
                id = UUID(db_product_id)                            # change datatype str to UUID
                product_instance = UpdateProduct(**updated_product)  # change datatype dict to SQLModel 
                with Session(engine) as session:
                    product = session.get(Product, id) #exec(select(Product).where(Product.id==id)).first()
                    if product_instance.name:
                        product.name = product_instance.name
                    if product_instance.price:
                        product.price = product_instance.price
                    if product_instance.quantity:
                        product.quantity = product_instance.quantity
                    if product_instance.category:
                        product.category = product_instance.category
                    # final_updated_product = product_instance.model_dump(exclude_unset=True)   # filter the data, removing None value
                    # product.sqlmodel_update(final_updated_product)
                    session.add(product)
                    session.commit()

        elif topic=="mart-product-increase-topic":
            async for message in consumer:
                dict_data = json.loads(message.value)
                id = UUID(dict_data.pop("id"))
                product_instance = Product(id=id, **dict_data) # Updated product
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==id)).first()
                    product.quantity = product_instance.quantity
                    session.add(product)
                    session.commit()
        
        else:
            raise HTTPException(status_code=500, detail=f"Internal Issue, topic {topic} not found ",)

    finally:
        await consumer.stop()


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating table")
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(kafka_consumer("mart-order-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-decrease-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-product-increase-topic", "broker:19092"))
    asyncio.create_task(kafka_consumer("mart-update-product-topic", "broker:19092"))
    print("table created")
    yield

app: FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

categories = ["food", "health", "fashion", "electronics", "sports", "vahicle", "furniture", "literature", "other"]


@app.post("/add-product")
async def add_product(product: ProductReq, producer: Annotated[Session, Depends(get_producer) ] ):
    if product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")
    ready_product = Product(name=product.name, price=product.price, category=product.category, quantity=product.quantity)
    
    # SQLModel to Json
    product_dict = ready_product.to_dict()
    json_product = json.dumps(product_dict).encode("utf-8")
    
    # Kafka
    await producer.send_and_wait("mart-product-topic", json_product) 
    return ready_product
 
@app.post("/order/")
async def order_place(order:Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[Session, Depends(get_producer) ]):
    product: Product | None = session.exec(select(Product).where(Product.id==order.product_id)).first()
    if not product:
        raise HTTPException(status_code=402, detail="product does not exist")
    if product.quantity < int(order.quantity):
        raise HTTPException(status_code=402, detail=f"Sorry, we have only {product.quantity} item of {product.name}")
    new_order = OrderPlace(product_id=order.product_id, quantity=order.quantity, product_price=product.price, product_name=product.name, product_category=product.category, totle_price=(product.price * order.quantity) )
    
    # SQLModel to json
    order_dict = new_order.to_dict()
    json_order = json.dumps(order_dict).encode("utf-8")

    # Kafka
    await producer.send_and_wait("mart-order-topic", json_order) 
    await producer.send_and_wait("mart-product-decrease-topic", json_order)
    return new_order

@app.get("/")
def root():
    return {"Message":"Mart API Sourcecode"}

@app.get("/get-all-products", response_model=list[Product])
def all_products(session: Annotated[Session, Depends(get_session) ] ):
    products = session.exec(select(Product)).all()
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

@app.get("/get_orders", response_model=list[OrderPlace])
def get_orders( session: Annotated[Session, Depends(get_session)]):
    orders = session.exec(select(OrderPlace)).all()
    return orders

@app.patch("/increment_product_item/${product_id}", response_model=Product)
async def update_product_item(product_id: UUID, add_item: int, session: Annotated[Session, Depends(get_session) ], producer: Annotated[Session, Depends(get_producer) ]  ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    db_product.quantity += int(add_item)

    # SQLModel to json
    dict_product = db_product.to_dict()
    json_product = json.dumps(dict_product).encode("utf-8")

    # Kafka
    await producer.send_and_wait("mart-product-increase-topic", json_product)
    return db_product

@app.patch("/update_product/${product_id}")
async def update_product(product_id: UUID, product: UpdateProduct, session: Annotated[Session, Depends(get_session) ], producer: Annotated[Session, Depends(get_producer) ]  ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    updated_product = product.model_dump(exclude_unset=True)
    print("updated_product", updated_product)
    db_product.sqlmodel_update(updated_product) 
    print("db_product", db_product)
    if db_product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")

    # SQLModel datatype to dict
    dict_updated_product = product.to_dict()

    dict_products = {"updated_product":dict_updated_product, "db_product_id": str(db_product.id)}
     
    json_product = json.dumps(dict_products).encode("utf-8")
    print("json_product", json_product)

    # kafka
    await producer.send_and_wait("mart-update-product-topic", json_product)
    return db_product
