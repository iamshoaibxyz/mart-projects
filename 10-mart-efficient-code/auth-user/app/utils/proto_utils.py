from datetime import datetime
from uuid import UUID
from app.schemas.protos import all_proto_pb2 as pb
from app.models.all_models import OrderPlacedModel, CartModel, CompanyModel, CompanyTokenModel, UserModel, UserTokenModel, InventoryTransaction, StockLevel, ProductModel, StockLevel
 
def user_to_proto(user: UserModel) -> pb.User:
    tokens = []
    orders = []
    carts = []
    if hasattr(user, 'tokens'):
        tokens = [user_token_to_proto(token) for token in user.tokens or []]
    if hasattr(user, 'orders'):
        orders = [order_to_proto(order) for order in user.orders or []]
    if hasattr(user, 'carts'):
        carts = [cart_to_proto(cart) for cart in user.carts or []]

    return pb.User(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email,
        is_verified=user.is_verified,
        verified_at=user.verified_at.isoformat() if user.verified_at else None,
        updated_at=user.updated_at.isoformat() if user.updated_at else None,
        created_at=user.created_at.isoformat(),
        # comments=[comment_to_proto(comment) for comment in user.comments or []],
        tokens=tokens,
        orders=orders,
        carts=carts
    )

def proto_to_user_model(user: pb.User) -> UserModel:
    tokens = []
    orders = []
    carts = []
    if hasattr(user, 'tokens'):
        tokens = [proto_to_user_token(token) for token in user.tokens]
    if hasattr(user, 'orders'):
        orders = [proto_to_order(order) for order in user.orders]
    if hasattr(user, 'carts'):
        carts = [proto_to_cart(cart) for cart in user.carts]
    return UserModel(
        id=UUID(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email,
        is_verified=user.is_verified,
        verified_at=datetime.fromisoformat(user.verified_at) if user.verified_at else None,
        updated_at=datetime.fromisoformat(user.updated_at) if user.updated_at else None,
        created_at=datetime.fromisoformat(user.created_at),
        tokens=tokens,
        orders=orders,
        # comments=[proto_to_comment(comment) for comment in user.comments],
        carts=carts
    )

def user_token_to_proto(token: UserTokenModel) -> pb.UserToken:
    return pb.UserToken(
        id=str(token.id),
        user_id=str(token.user_id) if token.user_id else "",
        token=token.token,
        created_at=token.created_at.isoformat(),
        expired_at=token.expired_at.isoformat()
    )

def proto_to_user_token(token: pb.UserToken) -> UserTokenModel:
    return UserTokenModel(
        id=UUID(token.id),
        user_id=UUID(token.user_id) if token.user_id else None,
        token=token.token,
        created_at=datetime.fromisoformat(token.created_at),
        expired_at=datetime.fromisoformat(token.expired_at)
    )

def company_to_proto(company: CompanyModel) -> pb.Company:
    tokens = []
    products = []
    if hasattr(company, 'tokens'):
        tokens = [company_token_to_proto(token) for token in company.tokens]
    if hasattr(company, 'products'):
        products = [product_to_proto(product) for product in company.products]

    return pb.Company(
        id=str(company.id),
        name=company.name,
        description=company.description,
        email=str(company.email),
        password=company.password,
        is_verified=company.is_verified,
        verified_at=company.verified_at.isoformat() if company.verified_at else "",
        created_at=company.created_at.isoformat(),
        updated_at=company.updated_at.isoformat() if company.updated_at else "",
        tokens=tokens,
        products=products
    )

def proto_to_company_model(company: pb.Company) -> CompanyModel:
    tokens = []
    products = []
    if hasattr(company, 'tokens'):
        tokens = [proto_to_company_token(token) for token in company.tokens]
    if hasattr(company, 'products'):
        products = [proto_to_product(product) for product in company.products]

    return CompanyModel(
        id=UUID(company.id),
        name=company.name,
        description=company.description,
        email=company.email,
        password=company.password,
        is_verified=company.is_verified,
        verified_at=datetime.fromisoformat(company.verified_at) if company.verified_at else None,
        created_at=datetime.fromisoformat(company.created_at),
        updated_at=datetime.fromisoformat(company.updated_at) if company.updated_at else None,
        tokens=tokens,
        products=products
    )

def company_token_to_proto(token: CompanyTokenModel) -> pb.CompanyToken:
    return pb.CompanyToken(
        id=str(token.id),
        company_id=str(token.company_id) if token.company_id else "",
        token=token.token,
        created_at=token.created_at.isoformat(),
        expired_at=token.expired_at.isoformat()
    )

def proto_to_company_token(token: pb.CompanyToken) -> CompanyTokenModel:
    return CompanyTokenModel(
        id=UUID(token.id),
        company_id=UUID(token.company_id) if token.company_id else None,
        token=token.token,
        created_at=datetime.fromisoformat(token.created_at),
        expired_at=datetime.fromisoformat(token.expired_at)
    )

def product_to_proto(product: ProductModel) -> pb.Product:
    return pb.Product(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        company_id=str(product.company_id),
        product_ranking=product.product_ranking,
        created_at=product.created_at.isoformat(),
        updated_at=product.updated_at.isoformat() if product.updated_at else "",
        # comments=[comment_to_proto(comment) for comment in product.comments or []],
        orders=[order_to_proto(order) for order in product.orders or []],
        stock=stock_level_to_proto(product.stock) if product.stock else None,
        transactions=[transaction_to_proto(tx) for tx in product.transactions or []]
    )

def proto_to_product(product: pb.Product) -> ProductModel:
    return ProductModel(
        id=UUID(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        company_id=UUID(product.company_id),
        product_ranking=product.product_ranking,
        created_at=datetime.fromisoformat(product.created_at),
        updated_at=datetime.fromisoformat(product.updated_at) if product.updated_at else None,
        # comments=[proto_to_comment(comment) for comment in product.comments],
        orders=[proto_to_order(order) for order in product.orders],
        stock=proto_to_stock_level(product.stock) if product.stock else None,
        transactions=[proto_to_transaction(tx) for tx in product.transactions]
    )

def cart_to_proto(cart: CartModel) -> pb.Cart:
    return pb.Cart(
        id=str(cart.id),
        user_id=str(cart.user_id),
        status=cart.status,
        created_at=cart.created_at.isoformat(),
        updated_at=cart.updated_at.isoformat(),
        orders=[order_to_proto(order) for order in cart.orders or []],
        total_price=cart.total_price
    )

def proto_to_cart(cart: pb.Cart) -> CartModel:
    return CartModel(
        id=UUID(cart.id),
        user_id=UUID(cart.user_id),
        status=cart.status,
        created_at=datetime.fromisoformat(cart.created_at),
        updated_at=datetime.fromisoformat(cart.updated_at),
        orders=[proto_to_order(order) for order in cart.orders],
        total_price=cart.total_price
    )
 
def order_to_proto(order: OrderPlacedModel) -> pb.Order:
    return pb.Order(
        id=str(order.id),
        cart_id=str(order.cart_id),
        user_id=str(order.user_id),
        product_id=str(order.product_id),
        product_price=order.product_price,
        quantity=order.quantity,
        total_price=order.total_price,
        order_date=order.order_date.isoformat(),
        delivery_date=order.delivery_date.isoformat() if order.delivery_date else "",
        delivered=order.delivered,
        status=order.status,
        return_back=order.return_back.isoformat() if order.return_back else "",
        delivery_address=order.delivery_address,
        created_at=order.created_at.isoformat(),
        updated_at=order.updated_at.isoformat()
    )

def proto_to_order(order: pb.Order) -> OrderPlacedModel:
    return OrderPlacedModel(
        id=UUID(order.id),
        cart_id=UUID(order.cart_id),
        user_id=UUID(order.user_id),
        product_id=UUID(order.product_id),
        product_price=order.product_price,
        quantity=order.quantity,
        total_price=order.total_price,
        order_date=datetime.fromisoformat(order.order_date),
        delivery_date=datetime.fromisoformat(order.delivery_date) if order.delivery_date else None,
        delivered=order.delivered,
        status=order.status,
        return_back=datetime.fromisoformat(order.return_back) if order.return_back else None,
        delivery_address=order.delivery_address,
        created_at=datetime.fromisoformat(order.created_at),
        updated_at=datetime.fromisoformat(order.updated_at)
    )

def stock_level_to_proto(stock: StockLevel) -> pb.StockLevel:
    return pb.StockLevel(
        id=str(stock.id),
        product_id=str(stock.product_id),
        quantity=stock.quantity,
        status=stock.status,
        created_at=stock.created_at.isoformat(),
        updated_at=stock.updated_at.isoformat() if stock.updated_at else "",
        product=product_to_proto(stock.product) if stock.product else None,
        transactions=[transaction_to_proto(transaction) for transaction in stock.transactions or []],

    )

def proto_to_stock_level(stock: pb.StockLevel) -> StockLevel:
    return StockLevel(
        id=UUID(stock.id),
        product_id=UUID(stock.product_id),
        quantity=stock.quantity,
        status=stock.status,
        created_at=datetime.fromisoformat(stock.created_at),
        updated_at=datetime.fromisoformat(stock.updated_at) if stock.updated_at else None,        
        product=proto_to_product(stock.product) if stock.product else None,
        transactions=[proto_to_transaction(transaction) for transaction in stock.transactions],
    )

def transaction_to_proto(transaction: InventoryTransaction) -> pb.InventoryTransaction:
    return pb.InventoryTransaction(
        id=str(transaction.id),
        product_id=str(transaction.product_id),
        operation=transaction.operation,
        quantity=transaction.quantity,
        created_at=transaction.created_at.isoformat(),
        updated_at=transaction.updated_at.isoformat() if transaction.updated_at else "",
        product=product_to_proto(transaction.product) if transaction.product else None,
        stock=stock_level_to_proto(transaction.stock) if transaction.stock else None,
    )

def proto_to_transaction(transaction: pb.InventoryTransaction) -> InventoryTransaction:
    return InventoryTransaction(
        id=UUID(transaction.id),
        product_id=UUID(transaction.product_id),
        operation=transaction.operation,
        quantity=transaction.quantity,
        created_at=datetime.fromisoformat(transaction.created_at),
        updated_at=datetime.fromisoformat(transaction.updated_at) if transaction.updated_at else None,
        product=proto_to_product(transaction.product) if transaction.product else None,
        stock=proto_to_stock_level(transaction.stock) if transaction.stock else None,
    )

