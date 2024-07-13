Here's the `.proto` file updated to use strings in ISO 8601 format (`.isoformat`) for datetime fields:

```proto
syntax = "proto3";

package models;

message Company {
    string id = 1;
    string name = 2;
    string description = 3;
    string email = 4;
    string password = 5;
    bool is_verified = 6;
    string verified_at = 7; // ISO 8601 format
    repeated CompanyToken tokens = 8;
    string created_at = 9; // ISO 8601 format
    string updated_at = 10; // ISO 8601 format
    repeated Product products = 11;
}

message CompanyToken {
    string id = 1;
    string company_id = 2;
    string token = 3;
    string created_at = 4; // ISO 8601 format
    string expired_at = 5; // ISO 8601 format
}

message User {
    string id = 1;
    string first_name = 2;
    string last_name = 3;
    string password = 4;
    string email = 5;
    bool is_verified = 6;
    string verified_at = 7; // ISO 8601 format
    string updated_at = 8; // ISO 8601 format
    string created_at = 9; // ISO 8601 format
    repeated UserToken tokens = 10;
    repeated OrderPlaced orders = 11;
    repeated Comment comments = 12;
}

message UserToken {
    string id = 1;
    string user_id = 2;
    string token = 3;
    string created_at = 4; // ISO 8601 format
    string expired_at = 5; // ISO 8601 format
}

message Comment {
    string id = 1;
    string user_id = 2;
    string product_id = 3;
    string comment_text = 4;
    float rating = 5;
    string created_at = 6; // ISO 8601 format
    string updated_at = 7; // ISO 8601 format
}

message Email {
    string id = 1;
    string recipient_email = 2;
    string subject = 3;
    string sent_at = 4; // ISO 8601 format
    string status = 5;
    repeated EmailContent contents = 6;
}

message EmailContent {
    string id = 1;
    string content = 2;
    string email_id = 3;
}

message Product {
    string id = 1;
    string name = 2;
    string description = 3;
    float price = 4;
    string company_id = 5;
    float product_ranking = 6;
    int32 stock = 7;
    string created_at = 8; // ISO 8601 format
    string updated_at = 9; // ISO 8601 format
    repeated Comment comments = 10;
    repeated OrderPlaced orders = 11;
    repeated Inventory inventories = 12;
}

enum OrderStatus {
    PENDING = 0;
    PROCESSING = 1;
    SHIPPED = 2;
    DELIVERED = 3;
    CANCELLED = 4;
}

message OrderPlaced {
    string id = 1;
    string user_id = 2;
    string product_id = 3;
    float product_price = 4;
    int32 quantity = 5;
    float total_price = 6;
    string order_date = 7; // ISO 8601 format
    string delivery_date = 8; // ISO 8601 format
    bool delivered = 9;
    OrderStatus status = 10;
    string return_back = 11; // ISO 8601 format
    string delivery_address = 12;
    string created_at = 13; // ISO 8601 format
    string updated_at = 14; // ISO 8601 format
}

message Inventory {
    string id = 1;
    string product_id = 2;
    int32 quantity = 3;
    string created_at = 4; // ISO 8601 format
    string updated_at = 5; // ISO 8601 format
}
```

### Explanation:

- All datetime fields (`created_at`, `updated_at`, `verified_at`, etc.) are represented as `string` with ISO 8601 format comments.
- The rest of the fields remain the same, ensuring the structure corresponds to the original SQLModel definitions.



-----------------------------------------------------------------------------------------



Here's a set of conversion functions for each of the models, similar to the `user_to_proto` and `proto_to_usermodel` functions you provided.

```python
from datetime import datetime
from uuid import UUID

import user_pb2  # Replace with the actual generated protobuf module import
import company_pb2  # Replace with the actual generated protobuf module import

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

def company_to_proto(company: CompanyModel) -> company_pb2.Company:
    company_proto = company_pb2.Company(
        id=str(company.id),
        name=company.name,
        description=company.description or "",
        email=company.email,
        password=company.password,
        is_verified=company.is_verified,
        verified_at=company.verified_at.isoformat() if company.verified_at else "",
        created_at=company.created_at.isoformat(),
        updated_at=company.updated_at.isoformat() if company.updated_at else ""
    )
    for token in company.tokens:
        company_proto.tokens.append(company_token_to_proto(token))
    for product in company.products:
        company_proto.products.append(product_to_proto(product))
    return company_proto

def proto_to_companymodel(company_proto: company_pb2.Company) -> CompanyModel:
    company = CompanyModel(
        id=UUID(company_proto.id),
        name=company_proto.name,
        description=company_proto.description or None,
        email=company_proto.email,
        password=company_proto.password,
        is_verified=company_proto.is_verified,
        verified_at=datetime.fromisoformat(company_proto.verified_at) if company_proto.verified_at else None,
        created_at=datetime.fromisoformat(company_proto.created_at),
        updated_at=datetime.fromisoformat(company_proto.updated_at) if company_proto.updated_at else None
    )
    company.tokens = [proto_to_companytoken(token_proto) for token_proto in company_proto.tokens]
    company.products = [proto_to_productmodel(product_proto) for product_proto in company_proto.products]
    return company

def company_token_to_proto(token: CompanyTokenModel) -> company_pb2.CompanyToken:
    token_proto = company_pb2.CompanyToken(
        id=str(token.id),
        company_id=str(token.company_id) if token.company_id else "",
        token=token.token,
        created_at=token.created_at.isoformat(),
        expired_at=token.expired_at.isoformat()
    )
    return token_proto

def proto_to_companytoken(token_proto: company_pb2.CompanyToken) -> CompanyTokenModel:
    token = CompanyTokenModel(
        id=UUID(token_proto.id),
        company_id=UUID(token_proto.company_id) if token_proto.company_id else None,
        token=token_proto.token,
        created_at=datetime.fromisoformat(token_proto.created_at),
        expired_at=datetime.fromisoformat(token_proto.expired_at)
    )
    return token

def product_to_proto(product: ProductModel) -> company_pb2.Product:
    product_proto = company_pb2.Product(
        id=str(product.id),
        name=product.name,
        description=product.description or "",
        price=product.price,
        company_id=str(product.company_id),
        product_ranking=product.product_ranking,
        stock=product.stock,
        created_at=product.created_at.isoformat(),
        updated_at=product.updated_at.isoformat() if product.updated_at else ""
    )
    for comment in product.comments:
        product_proto.comments.append(comment_to_proto(comment))
    for order in product.orders:
        product_proto.orders.append(order_to_proto(order))
    for inventory in product.inventories:
        product_proto.inventories.append(inventory_to_proto(inventory))
    return product_proto

def proto_to_productmodel(product_proto: company_pb2.Product) -> ProductModel:
    product = ProductModel(
        id=UUID(product_proto.id),
        name=product_proto.name,
        description=product_proto.description or None,
        price=product_proto.price,
        company_id=UUID(product_proto.company_id),
        product_ranking=product_proto.product_ranking,
        stock=product_proto.stock,
        created_at=datetime.fromisoformat(product_proto.created_at),
        updated_at=datetime.fromisoformat(product_proto.updated_at) if product_proto.updated_at else None
    )
    product.comments = [proto_to_commentmodel(comment_proto) for comment_proto in product_proto.comments]
    product.orders = [proto_to_orderplacedmodel(order_proto) for order_proto in product_proto.orders]
    product.inventories = [proto_to_inventorymodel(inventory_proto) for inventory_proto in product_proto.inventories]
    return product

def comment_to_proto(comment: CommentModel) -> company_pb2.Comment:
    comment_proto = company_pb2.Comment(
        id=str(comment.id),
        user_id=str(comment.user_id),
        product_id=str(comment.product_id),
        comment_text=comment.comment_text,
        rating=comment.rating,
        created_at=comment.created_at.isoformat(),
        updated_at=comment.updated_at.isoformat()
    )
    return comment_proto

def proto_to_commentmodel(comment_proto: company_pb2.Comment) -> CommentModel:
    comment = CommentModel(
        id=UUID(comment_proto.id),
        user_id=UUID(comment_proto.user_id),
        product_id=UUID(comment_proto.product_id),
        comment_text=comment_proto.comment_text,
        rating=comment_proto.rating,
        created_at=datetime.fromisoformat(comment_proto.created_at),
        updated_at=datetime.fromisoformat(comment_proto.updated_at)
    )
    return comment

def order_to_proto(order: OrderPlacedModel) -> company_pb2.OrderPlaced:
    order_proto = company_pb2.OrderPlaced(
        id=str(order.id),
        user_id=str(order.user_id),
        product_id=str(order.product_id),
        product_price=order.product_price,
        quantity=order.quantity,
        total_price=order.total_price,
        order_date=order.order_date.isoformat(),
        delivery_date=order.delivery_date.isoformat() if order.delivery_date else "",
        delivered=order.delivered,
        status=company_pb2.OrderStatus.Value(order.status.name),
        return_back=order.return_back.isoformat() if order.return_back else "",
        delivery_address=order.delivery_address,
        created_at=order.created_at.isoformat(),
        updated_at=order.updated_at.isoformat()
    )
    return order_proto

def proto_to_orderplacedmodel(order_proto: company_pb2.OrderPlaced) -> OrderPlacedModel:
    order = OrderPlacedModel(
        id=UUID(order_proto.id),
        user_id=UUID(order_proto.user_id),
        product_id=UUID(order_proto.product_id),
        product_price=order_proto.product_price,
        quantity=order_proto.quantity,
        total_price=order_proto.total_price,
        order_date=datetime.fromisoformat(order_proto.order_date),
        delivery_date=datetime.fromisoformat(order_proto.delivery_date) if order_proto.delivery_date else None,
        delivered=order_proto.delivered,
        status=OrderStatus(order_proto.status),
        return_back=datetime.fromisoformat(order_proto.return_back) if order_proto.return_back else None,
        delivery_address=order_proto.delivery_address,
        created_at=datetime.fromisoformat(order_proto.created_at),
        updated_at=datetime.fromisoformat(order_proto.updated_at)
    )
    return order

def inventory_to_proto(inventory: InventoryModel) -> company_pb2.Inventory:
    inventory_proto = company_pb2.Inventory(
        id=str(inventory.id),
        product_id=str(inventory.product_id),
        quantity=inventory.quantity,
        created_at=inventory.created_at.isoformat(),
        updated_at=inventory.updated_at.isoformat() if inventory.updated_at else ""
    )
    return inventory_proto

def proto_to_inventorymodel(inventory_proto: company_pb2.Inventory) -> InventoryModel:
    inventory = InventoryModel(
        id=UUID(inventory_proto.id),
        product_id=UUID(inventory_proto.product_id),
        quantity=inventory_proto.quantity,
        created_at=datetime.fromisoformat(inventory_proto.created_at),
        updated_at=datetime.fromisoformat(inventory_proto.updated_at) if inventory_proto.updated_at else None
    )
    return inventory
```

### Explanation:

- **CompanyModel and CompanyTokenModel**: Conversion functions `company_to_proto` and `proto_to_companymodel` include nested conversions for related models like `tokens` and `products`.
- **ProductModel**: Conversion functions `product_to_proto` and `proto_to_productmodel` include nested conversions for related models like `comments`, `orders`, and `inventories`.
- **OrderStatus**: The enum conversion uses `company_pb2.OrderStatus.Value` and `OrderStatus` for mapping between proto and model enums.
- **Datetime fields**: All datetime fields are converted to and from ISO 8601 string format.
- **UUID fields**: UUID fields are converted to strings and vice versa.

Replace the `user_pb2`, `company_pb2`, and other necessary imports with the actual protobuf modules generated for your models. This way, you can handle conversions between your SQLModel

 models and protobuf messages seamlessly.


====================================================================================================


Writing all `.proto` definitions in a single file can be convenient for small projects. However, for larger projects with many messages and services, it's generally better to organize the `.proto` definitions into multiple files. This approach offers several benefits:

1. **Maintainability**: Easier to manage and update specific parts of the protobuf schema without affecting unrelated parts.
2. **Reusability**: Common messages and enums can be defined in separate files and imported where needed, promoting reusability.
3. **Clarity**: Each file can be focused on a specific domain or service, making the codebase easier to understand.

For your project, you could organize the `.proto` files based on your domain models and services. Here's an example structure:

```
protos/
├── common.proto
├── user.proto
├── company.proto
├── product.proto
├── order.proto
├── inventory.proto
```

### Example `.proto` Files

#### `common.proto`
```proto
syntax = "proto3";

package common;

message UUID {
  string value = 1;
}

message Timestamp {
  string value = 1;  // ISO 8601 format
}
```

#### `user.proto`
```proto
syntax = "proto3";

package user;

import "common.proto";

message User {
  common.UUID id = 1;
  string first_name = 2;
  string last_name = 3;
  string password = 4;
  string email = 5;
  bool is_verified = 6;
  common.Timestamp verified_at = 7;
  common.Timestamp updated_at = 8;
  common.Timestamp created_at = 9;
}
```

#### `company.proto`
```proto
syntax = "proto3";

package company;

import "common.proto";
import "product.proto";

message Company {
  common.UUID id = 1;
  string name = 2;
  string description = 3;
  string email = 4;
  string password = 5;
  bool is_verified = 6;
  common.Timestamp verified_at = 7;
  common.Timestamp created_at = 8;
  common.Timestamp updated_at = 9;
  repeated CompanyToken tokens = 10;
  repeated product.Product products = 11;
}

message CompanyToken {
  common.UUID id = 1;
  common.UUID company_id = 2;
  string token = 3;
  common.Timestamp created_at = 4;
  common.Timestamp expired_at = 5;
}
```

#### `product.proto`
```proto
syntax = "proto3";

package product;

import "common.proto";
import "company.proto";
import "comment.proto";
import "order.proto";
import "inventory.proto";

message Product {
  common.UUID id = 1;
  string name = 2;
  string description = 3;
  float price = 4;
  common.UUID company_id = 5;
  float product_ranking = 6;
  int32 stock = 7;
  common.Timestamp created_at = 8;
  common.Timestamp updated_at = 9;
  repeated comment.Comment comments = 10;
  repeated order.OrderPlaced orders = 11;
  repeated inventory.Inventory inventories = 12;
}
```

#### `order.proto`
```proto
syntax = "proto3";

package order;

import "common.proto";
import "product.proto";

enum OrderStatus {
  PENDING = 0;
  PROCESSING = 1;
  SHIPPED = 2;
  DELIVERED = 3;
  CANCELLED = 4;
}

message OrderPlaced {
  common.UUID id = 1;
  common.UUID user_id = 2;
  common.UUID product_id = 3;
  float product_price = 4;
  int32 quantity = 5;
  float total_price = 6;
  common.Timestamp order_date = 7;
  common.Timestamp delivery_date = 8;
  bool delivered = 9;
  OrderStatus status = 10;
  common.Timestamp return_back = 11;
  string delivery_address = 12;
  common.Timestamp created_at = 13;
  common.Timestamp updated_at = 14;
}
```

#### `inventory.proto`
```proto
syntax = "proto3";

package inventory;

import "common.proto";
import "product.proto";

message Inventory {
  common.UUID id = 1;
  common.UUID product_id = 2;
  int32 quantity = 3;
  common.Timestamp created_at = 4;
  common.Timestamp updated_at = 5;
}
```

### Updating Conversion Functions
Make sure to update the conversion functions to match the new `.proto` definitions.

This modular approach keeps the project organized and manageable as it grows. It also makes it easier for multiple developers to work on different parts of the system concurrently.
