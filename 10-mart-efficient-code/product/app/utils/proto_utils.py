from datetime import datetime, timezone
from uuid import UUID
from app.schemas.protos import all_proto_pb2
from app.models.all_models import CompanyModel, CompanyTokenModel, UserModel, UserTokenModel, ProductModel, StockLevel, InventoryTransaction
import enum

def user_to_proto(user: UserModel) -> all_proto_pb2.User:
    user_proto = all_proto_pb2.User(
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

def proto_to_user(user_proto: all_proto_pb2.User) -> UserModel:
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

def user_token_to_proto(user_token: UserTokenModel) -> all_proto_pb2.UserToken:
    return all_proto_pb2.UserToken(
        id=str(user_token.id),
        user_id=str(user_token.user_id),
        token=user_token.token,
        created_at=user_token.created_at.isoformat(),
        expired_at=user_token.expired_at.isoformat(),
    )

def proto_to_user_token(proto_user_token: all_proto_pb2.UserToken) -> UserTokenModel:
    return UserTokenModel(
        id=UUID(proto_user_token.id),
        token=proto_user_token.token,
        user_id=UUID(proto_user_token.user_id),
        created_at=datetime.fromisoformat(proto_user_token.created_at),
        expired_at=datetime.fromisoformat(proto_user_token.expired_at),
    )

def company_to_proto(company: CompanyModel) -> all_proto_pb2.Company:
    return all_proto_pb2.Company(
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

def proto_to_company(proto_company: all_proto_pb2.Company) -> CompanyModel:
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

def company_token_to_proto(company_token: CompanyTokenModel) -> all_proto_pb2.CompanyToken:
    return all_proto_pb2.CompanyToken(
        id=str(company_token.id),
        company_id=str(company_token.company_id),
        token=company_token.token,
        created_at=company_token.created_at.isoformat(),
        expired_at=company_token.expired_at.isoformat(),
    )

def proto_to_company_token(proto_company_token: all_proto_pb2.CompanyToken) -> CompanyTokenModel:
    return CompanyTokenModel(
        id=UUID(proto_company_token.id),
        company_id=UUID(proto_company_token.company_id) if proto_company_token.company_id else None,
        token=proto_company_token.token,
        created_at=datetime.fromisoformat(proto_company_token.created_at),
        expired_at=datetime.fromisoformat(proto_company_token.expired_at)
        )

def product_to_proto(product: ProductModel) -> all_proto_pb2.Product:
    return all_proto_pb2.Product(
        id=str(product.id),
        name=product.name,
        description=product.description or "",
        price=product.price,
        category=product.category,
        company_id=str(product.company_id),
        product_ranking=product.product_ranking or 0.0,
        created_at=product.updated_at.isoformat(),
        updated_at=product.updated_at.isoformat() if product.updated_at else datetime.now(timezone.utc).isoformat(),
        # stock=stocklevel_to_proto(product.stock) if product.stock else None,
        # transactions=[inventory_transaction_to_proto(tx) for tx in product.transactions or []]
        # for comment in product.comments:
        #     product_proto.comments.append(comment_to_proto(comment))
        # for order in product.orders:
        #     product_proto.orders.append(order_to_proto(order))
    )
 
def proto_to_productmodel(proto: all_proto_pb2.Product) -> ProductModel:
    product = ProductModel(
        id=UUID(proto.id),
        name=proto.name,
        description=proto.description  or None,
        price=proto.price,
        category=proto.category,
        company_id=UUID(proto.company_id),
        product_ranking=proto.product_ranking,
        created_at=datetime.fromisoformat(proto.created_at),
        updated_at=datetime.fromisoformat(proto.updated_at),
        stock=proto_to_stocklevel(proto.stock) if proto.HasField("stock") else None,
        transactions=[proto_to_inventory_transaction(tx) for tx in proto.transactions],
        # product.comments = [proto_to_commentmodel(comment_proto) for comment_proto in product_proto.comments],
        # product.orders = [proto_to_orderplacedmodel(order_proto) for order_proto in product_proto.orders]
    )
    return product

 
def stocklevel_to_proto(stock: StockLevel) -> all_proto_pb2.StockLevel:
    return all_proto_pb2.StockLevel(
        id=str(stock.id),
        product_id=str(stock.product_id),
        current_stock=stock.current_stock,
        created_at=stock.updated_at.isoformat(),
        updated_at=stock.updated_at.isoformat() if stock.updated_at else datetime.now(timezone.utc).isoformat(),
        transactions=[inventory_transaction_to_proto(tx) for tx in stock.transactions or []]
    )
  
def proto_to_stocklevel(proto: all_proto_pb2.StockLevel) -> StockLevel:
    stock = StockLevel(
        id=UUID(proto.id),
        product_id=UUID(proto.product_id),
        current_stock=proto.current_stock,
        created_at=datetime.fromisoformat(proto.created_at),
        updated_at=datetime.fromisoformat(proto.updated_at),
        transactions=[proto_to_inventory_transaction(tx) for tx in proto.transactions]
    )
    return stock

class Operation(enum.Enum):
    ADD = "add"
    SUBTRACT = "subtract"
 
def inventory_transaction_to_proto(transaction: InventoryTransaction) -> all_proto_pb2.InventoryTransaction:
    operation_map = {
        Operation.ADD: all_proto_pb2.InventoryTransaction.Operation.ADD,
        Operation.SUBTRACT: all_proto_pb2.InventoryTransaction.Operation.SUBTRACT
    }
    
    if transaction.operation not in operation_map:
        raise ValueError(f"Unknown operation: {transaction.operation}")
    
    return all_proto_pb2.InventoryTransaction(
        id=str(transaction.id),
        stock_id=str(transaction.stock_id),
        product_id=str(transaction.product_id),
        quantity=transaction.quantity,
        timestamp=transaction.timestamp.isoformat(),
        operation=operation_map[transaction.operation],
        stock=stocklevel_to_proto(transaction.stock) if transaction.stock else None,
        product=product_to_proto(transaction.product) if transaction.product else None
    )

 
def proto_to_inventory_transaction(proto: all_proto_pb2.InventoryTransaction) -> InventoryTransaction:
    transaction = InventoryTransaction(
        id=UUID(proto.id),
        stock_id=UUID(proto.stock_id),
        product_id=UUID(proto.product_id),
        quantity=proto.quantity,
        timestamp=datetime.fromisoformat(proto.timestamp),
        operation=Operation(proto.operation.name.lower()),
        stock=proto_to_stocklevel(proto.stock) if proto.HasField("stock") else None,
        product=proto_to_productmodel(proto.product) if proto.HasField("product") else None
    )
    return transaction

 


