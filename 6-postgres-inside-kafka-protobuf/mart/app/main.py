

from fastapi import FastAPI, HTTPException, Depends
from app import setting, mart_pb2
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
                new_product = mart_pb2.Product()
                new_product.ParseFromString(message.value)
                product_data = {
                "id": UUID(new_product.id),
                "name": new_product.name,
                "category": new_product.category,
                "price": new_product.price,
                "quantity": new_product.quantity
                }
                product_instance = Product(**product_data)
                with Session(engine) as session:               
                    session.add(product_instance)
                    session.commit()

        elif topic=="mart-order-topic":
            async for message in consumer:
                new_order = mart_pb2.Order()
                new_order.ParseFromString(message.value)
                order_data = { 
                    "product_id":UUID(new_order.product_id), 
                    "order_id":UUID(new_order.order_id), 
                    "product_name": new_order.product_name, 
                    "product_category": new_order.product_category, 
                    "quantity":new_order.quantity, 
                    "product_price": new_order.product_price, 
                    "totle_price": new_order.totle_price}    

                # Initialize the Product instance using the extracted id
                Order_instance = OrderPlace(**order_data) 
                with Session(engine) as session:   
                    session.add(Order_instance)
                    session.commit()

        elif topic=="mart-product-decrease-topic":
            async for message in consumer:
                new_order = mart_pb2.Order()
                new_order.ParseFromString(message.value)
                order_data = { 
                    "product_id":UUID(new_order.product_id), 
                    "order_id":UUID(new_order.order_id), 
                    "product_name": new_order.product_name, 
                    "product_category": new_order.product_category, 
                    "quantity":new_order.quantity, 
                    "product_price": new_order.product_price, 
                    "totle_price": new_order.totle_price}
                product_instance = OrderPlace(**order_data) 
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==product_instance.product_id)).first() #get(Product, product_instance.product_id)
                    product.quantity -= product_instance.quantity 
                    session.add(product)
                    session.commit()

        elif topic=="mart-update-product-topic":
            async for message in consumer:
                new_product = mart_pb2.UpdateProduct()
                new_product.ParseFromString(message.value)
                id=UUID(new_product.id)

                updated_product = {
                "name": new_product.name ,
                "category": new_product.category ,
                "price": new_product.price ,
                "quantity": new_product.quantity }

                product_instance = UpdateProduct(**updated_product)  # change datatype dict to SQLModel 
                with Session(engine) as session:
                    product = session.get(Product, id) #exec(select(Product).where(Product.id==id)).first()
                    product.name = product_instance.name if product_instance.name else product.name
                    product.price = product_instance.price if product_instance.price else product.price
                    product.quantity = product_instance.quantity if product_instance.quantity else product.quantity
                    product.category = product_instance.category if product_instance.category else product.category
                    session.add(product)
                    session.commit()
                #     # final_updated_product = product_instance.model_dump(exclude_unset=True)   # filter the data, removing None value
                #     # product.sqlmodel_update(final_updated_product)

        elif topic=="mart-product-increase-topic":
            async for message in consumer:
                new_inc_product = mart_pb2.IncrementProductItem()
                new_inc_product.ParseFromString(message.value)
                id = UUID(new_inc_product.id)
                with Session(engine) as session:
                    product = session.exec(select(Product).where(Product.id==id)).first()
                    product.quantity += new_inc_product.add_product
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
    
    # SQLModel to protobuf
    product_protobuf = mart_pb2.Product(id=str(ready_product.id), name= ready_product.name, price=ready_product.price, category= ready_product.category, quantity= ready_product.quantity)
    serialized_product = product_protobuf.SerializeToString()
    
    # Kafka
    await producer.send_and_wait("mart-product-topic", serialized_product) 
    return ready_product
 
@app.post("/order/")
async def order_place(order:Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[Session, Depends(get_producer) ]):
    product: Product | None = session.exec(select(Product).where(Product.id==order.product_id)).first()
    if not product:
        raise HTTPException(status_code=402, detail="product does not exist")
    if product.quantity < int(order.quantity):
        raise HTTPException(status_code=402, detail=f"Sorry, we have only {product.quantity} item of {product.name}")
    new_order = OrderPlace(product_id=order.product_id, quantity=order.quantity, product_price=product.price, product_name=product.name, product_category=product.category, totle_price=(product.price * order.quantity) )
    
    # SQLModel to protobuf
    order_protobuf = mart_pb2.Order(product_id=str(new_order.product_id), order_id=str(new_order.order_id), product_name= new_order.product_name, product_category= new_order.product_category, quantity=new_order.quantity, product_price= new_order.product_price, totle_price= new_order.totle_price)
    serialized_order = order_protobuf.SerializeToString()
    

    # Kafka
    await producer.send_and_wait("mart-order-topic", serialized_order) 
    await producer.send_and_wait("mart-product-decrease-topic", serialized_order)
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

    # SQLModel to protobuf
    add_product_protobuf = mart_pb2.IncrementProductItem(id=str(db_product.id), add_product=add_item)
    serialized_product = add_product_protobuf.SerializeToString()
    # Kafka
    await producer.send_and_wait("mart-product-increase-topic", serialized_product)
    return db_product

@app.patch("/update_product/${product_id}")
async def update_product(product_id: UUID, product: UpdateProduct, session: Annotated[Session, Depends(get_session) ], producer: Annotated[Session, Depends(get_producer) ]  ):
    db_product = session.exec(select(Product).where(Product.id==product_id)).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    updated_product = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(updated_product)
    if db_product.category not in categories:
        raise HTTPException(status_code=402, detail="Add a specific keyword")

    # SQLModel datatype to product
    protobuf_product = mart_pb2.UpdateProduct(
        id=str(db_product.id),
        name=product.name if product.name else None,
        category=product.category if product.category else None,
        price=product.price if product.price else None,
        quantity=product.quantity if product.quantity else None
    )
    serialized_product = protobuf_product.SerializeToString()

    # kafka
    await producer.send_and_wait("mart-update-product-topic", serialized_product)
    return db_product
