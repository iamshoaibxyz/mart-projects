from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    name: str
    category: str = Field(default='food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: int
    quantity : int

class UpdateProduct(SQLModel):
    name: None| str = Field(None)
    category: None| str = Field(default='food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: None| int = Field(None)
    quantity : None| int = Field(None)

class Order(SQLModel):
    product_id: int
    quantity: int

class OrderPlace(Order, table=True):
    order_id: int | None = Field(None, primary_key=True)    
    product_price: int
    product_name: str
    product_category: str
    totle_price: int

class OrderReq(Order):
    pass