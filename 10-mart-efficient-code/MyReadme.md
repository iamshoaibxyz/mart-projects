"""REGISTRY_URL = 'http://localhost:8082/apis/registry/v2/groups/default/artifacts/`"""

import requests

def register_schema(schema, schema_name, content_type="application/json"):
    url = "http://localhost:8080/apis/registry/v2/groups/default/artifacts"
    headers = {
        "Content-Type": content_type,
        "X-Registry-ArtifactId": schema_name,
    }
    response = requests.post(url, headers=headers, data=schema)
    response.raise_for_status()
    return response.json()

package user;

import "google/protobuf/timestamp.proto";

// User message definition
message CreateUser {
    string id = 1;
    string first_name = 2;
    string last_name = 3;
    string password = 4;
    string email = 5;
    bool is_verified = 6;
    google.protobuf.Timestamp verified_at = 7;
    google.protobuf.Timestamp updated_at = 8;
    google.protobuf.Timestamp created_at = 9;
    repeated UserToken tokens = 10;
    repeated Order orders = 11;
    repeated Comment comments = 12;
}

// UserToken message definition
message UserToken {
    string id = 1;
    string user_id = 2;
    string token = 3;
    google.protobuf.Timestamp created_at = 4;
    google.protobuf.Timestamp expired_at = 5;
}

Sure! Here's a structured approach to creating `.proto` files, generating Python code, and implementing conversion functions for each SQLModel class.

### Step 1: Define Protobuf Messages

**1. CommentModel - comment.proto**
```proto
syntax = "proto3";

package comment;

message Comment {
    string id = 1;
    string user_id = 2;
    string product_id = 3;
    string comment_text = 4;
    float rating = 5;
    string created_at = 6;
    string updated_at = 7;
}
```

**2. EmailModel - email.proto**
```proto
syntax = "proto3";

package email;

message Email {
    string id = 1;
    string recipient_email = 2;
    string subject = 3;
    string sent_at = 4;
    string status = 5;
}
```

**3. EmailContentModel - email_content.proto**
```proto
syntax = "proto3";

package email_content;

message EmailContent {
    string id = 1;
    string content = 2;
    string email_id = 3;
}
```

**4. OrderPlacedModel - order.proto**
```proto
syntax = "proto3";

package order;

enum OrderStatus {
    PENDING = 0;
    PROCESSING = 1;
    SHIPPED = 2;
    DELIVERED = 3;
    CANCELLED = 4;
}

message Order {
    string id = 1;
    string user_id = 2;
    string product_id = 3;
    float product_price = 4;
    int quantity = 5;
    float total_price = 6;
    string order_date = 7;
    string delivery_date = 8;
    bool delivered = 9;
    OrderStatus status = 10;
    string return_back = 11;
    string delivery_address = 12;
    string created_at = 13;
    string updated_at = 14;
}
```

**5. ProductModel - product.proto**
```proto
syntax = "proto3";

package product;

message Product {
    string id = 1;
    string name = 2;
    string description = 3;
    float price = 4;
    string company_id = 5;
    float product_ranking = 6;
    int stock = 7;
    string created_at = 8;
    string updated_at = 9;
}
```

**6. CompanyModel - company.proto**
```proto
syntax = "proto3";

package company;

message Company {
    string id = 1;
    string name = 2;
    string description = 3;
    string email = 4;
    string password = 5;
    bool is_verified = 6;
    string verified_at = 7;
    string created_at = 8;
    string updated_at = 9;
}
```

**7. CompanyTokenModel - company_token.proto**
```proto
syntax = "proto3";

package company_token;

message CompanyToken {
    string id = 1;
    string company_id = 2;
    string token = 3;
    string created_at = 4;
    string expired_at = 5;
}
```

**8. UserModel - user.proto**
```proto
syntax = "proto3";

package user;

message User {
    string id = 1;
    string first_name = 2;
    string last_name = 3;
    string password = 4;
    string email = 5;
    bool is_verified = 6;
    string verified_at = 7;
    string updated_at = 8;
    string created_at = 9;
}
```

**9. UserTokenModel - user_token.proto**
```proto
syntax = "proto3";

package user_token;

message UserToken {
    string id = 1;
    string user_id = 2;
    string token = 3;
    string created_at = 4;
    string expired_at = 5;
}
```

### Step 2: Generate Python Code from Protobuf Files

Compile the `.proto` files to generate Python code. Use the `protoc` compiler:

```bash
protoc --python_out=./path_to_output_dir comment.proto
protoc --python_out=./path_to_output_dir email.proto
protoc --python_out=./path_to_output_dir email_content.proto
protoc --python_out=./path_to_output_dir order.proto
protoc --python_out=./path_to_output_dir product.proto
protoc --python_out=./path_to_output_dir company.proto
protoc --python_out=./path_to_output_dir company_token.proto
protoc --python_out=./path_to_output_dir user.proto
protoc --python_out=./path_to_output_dir user_token.proto
```

### Step 3: Implement Conversion Functions

Here are the conversion functions for each model:

**comment_pb2.py**
```python
import comment_pb2
from models import CommentModel
from uuid import UUID
from datetime import datetime

class CommentProtoConverter:
    @staticmethod
    def comment_to_proto(comment: CommentModel) -> comment_pb2.Comment:
        return comment_pb2.Comment(
            id=str(comment.id),
            user_id=str(comment.user_id),
            product_id=str(comment.product_id),
            comment_text=comment.comment_text,
            rating=comment.rating if comment.rating else 0.0,
            created_at=comment.created_at.isoformat(),
            updated_at=comment.updated_at.isoformat(),
        )

    @staticmethod
    def proto_to_comment(proto_comment: comment_pb2.Comment) -> CommentModel:
        return CommentModel(
            id=UUID(proto_comment.id),
            user_id=UUID(proto_comment.user_id),
            product_id=UUID(proto_comment.product_id),
            comment_text=proto_comment.comment_text,
            rating=proto_comment.rating if proto_comment.rating else 0.0,
            created_at=datetime.fromisoformat(proto_comment.created_at),
            updated_at=datetime.fromisoformat(proto_comment.updated_at),
        )
```

**email_pb2.py**
```python
import email_pb2
from models import EmailModel
from uuid import UUID
from datetime import datetime

class EmailProtoConverter:
    @staticmethod
    def email_to_proto(email: EmailModel) -> email_pb2.Email:
        return email_pb2.Email(
            id=str(email.id),
            recipient_email=email.recipient_email,
            subject=email.subject,
            sent_at=email.sent_at.isoformat(),
            status=email.status,
        )

    @staticmethod
    def proto_to_email(proto_email: email_pb2.Email) -> EmailModel:
        return EmailModel(
            id=UUID(proto_email.id),
            recipient_email=proto_email.recipient_email,
            subject=proto_email.subject,
            sent_at=datetime.fromisoformat(proto_email.sent_at),
            status=proto_email.status,
        )
```

**email_content_pb2.py**
```python
import email_content_pb2
from models import EmailContentModel
from uuid import UUID
from datetime import datetime

class EmailContentProtoConverter:
    @staticmethod
    def email_content_to_proto(email_content: EmailContentModel) -> email_content_pb2.EmailContent:
        return email_content_pb2.EmailContent(
            id=str(email_content.id),
            content=email_content.content,
            email_id=str(email_content.email_id),
        )

    @staticmethod
    def proto_to_email_content(proto_email_content: email_content_pb2.EmailContent) -> EmailContentModel:
        return EmailContentModel(
            id=UUID(proto_email_content.id),
            content=proto_email_content.content,
            email_id=UUID(proto_email_content.email_id),
        )
```

**order_pb2.py**
```python
import order_pb2
from models import OrderPlacedModel
from uuid import UUID
from datetime import datetime

class OrderProtoConverter:
    @staticmethod
    def order_to_proto(order: OrderPlacedModel) -> order_pb2.Order:
        return order_pb2.Order(
            id=str(order.id),
            user_id=str(order.user_id),
            product_id=str(order.product_id),
            product_price=order.product_price,
            quantity=order.quantity,
            total_price=order.total_price,
            order_date=order.order_date.isoformat(),
            delivery_date=order.delivery_date.isoformat() if order.delivery_date else "",
            delivered=order.delivered,
            status=order.status.value,
            return_back=order.return_back.isoformat() if order.return_back else "",
            delivery_address=order.delivery_address,
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )

    @staticmethod
    def proto_to_order(proto_order: order_pb2.Order) -> OrderPlacedModel:
        return OrderPlacedModel(
            id=UUID(proto_order.id),
            user_id=UUID(proto_order.user_id),
            product_id=UUID(proto_order.product_id),
            product_price=proto_order.product_price,
            quantity=proto_order.quantity,
            total_price=proto_order.total_price,
            order_date=datetime.fromisoformat(proto_order.order_date),
            delivery_date=datetime.fromisoformat(proto_order.delivery_date) if proto_order.delivery_date else None,
            delivered=proto_order.delivered,
            status=OrderStatus(proto_order.status),
            return_back=datetime.fromisoformat(proto_order.return_back) if proto_order.return_back else None,
            delivery_address=proto_order.delivery_address,
            created_at=datetime.fromisoformat(proto_order.created_at),
            updated_at=datetime.fromisoformat(proto_order.updated_at),
        )
```

**product_pb2.py**
```python
import product_pb2
from models import ProductModel
from uuid import UUID
from datetime import datetime

class ProductProtoConverter:
    @staticmethod
    def product_to_proto(product: ProductModel) -> product_pb2.Product:
        return product_pb2.Product(
            id=str(product.id),
            name=product.name,
            description=product

.description if product.description else "",
            price=product.price,
            company_id=str(product.company_id),
            product_ranking=product.product_ranking if product.product_ranking else 0.0,
            stock=product.stock,
            created_at=product.created_at.isoformat(),
            updated_at=product.updated_at.isoformat() if product.updated_at else "",
        )

    @staticmethod
    def proto_to_product(proto_product: product_pb2.Product) -> ProductModel:
        return ProductModel(
            id=UUID(proto_product.id),
            name=proto_product.name,
            description=proto_product.description if proto_product.description else None,
            price=proto_product.price,
            company_id=UUID(proto_product.company_id),
            product_ranking=proto_product.product_ranking if proto_product.product_ranking else 0.0,
            stock=proto_product.stock,
            created_at=datetime.fromisoformat(proto_product.created_at),
            updated_at=datetime.fromisoformat(proto_product.updated_at) if proto_product.updated_at else None,
        )
```

**company_pb2.py**
```python
import company_pb2
from models import CompanyModel
from uuid import UUID
from datetime import datetime

class CompanyProtoConverter:
    @staticmethod
    def company_to_proto(company: CompanyModel) -> company_pb2.Company:
        return company_pb2.Company(
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

    @staticmethod
    def proto_to_company(proto_company: company_pb2.Company) -> CompanyModel:
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
```

**company_token_pb2.py**
```python
import company_token_pb2
from models import CompanyTokenModel
from uuid import UUID
from datetime import datetime
 
 
class CompanyTokenProtoConverter:
    @staticmethod
    def company_token_to_proto(company_token: CompanyTokenModel) -> company_token_pb2.CompanyToken:
        return company_token_pb2.CompanyToken(
            id=str(company_token.id),
            company_id=str(company_token.company_id),
            token=company_token.token,
            created_at=company_token.created_at.isoformat(),
            expired_at=company_token.expired_at.isoformat(),
        )

    @staticmethod
    def proto_to_company_token(proto_company_token: company_token_pb2.CompanyToken) -> CompanyTokenModel:
        return CompanyTokenModel(
            id=UUID(proto_company_token.id),
            company_id=UUID(proto_company_token.company_id),
            token=proto_company_token.token,
            created_at=datetime.fromisoformat(proto_company_token.created_at),
            expired_at=datetime.fromisoformat(proto_company_token.expired_at),
        )
```

**user_pb2.py**
```python
import user_pb2
from models import UserModel
from uuid import UUID
from datetime import datetime

class UserProtoConverter:
    @staticmethod
    def user_to_proto(user: UserModel) -> user_pb2.User:
        return user_pb2.User(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            password=user.password,
            email=user.email,
            is_verified=user.is_verified,
            verified_at=user.verified_at.isoformat() if user.verified_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else "",
            created_at=user.created_at.isoformat(),
        )

    @staticmethod
    def proto_to_user(proto_user: user_pb2.User) -> UserModel:
        return UserModel(
            id=UUID(proto_user.id),
            first_name=proto_user.first_name,
            last_name=proto_user.last_name,
            password=proto_user.password,
            email=proto_user.email,
            is_verified=proto_user.is_verified,
            verified_at=datetime.fromisoformat(proto_user.verified_at) if proto_user.verified_at else None,
            updated_at=datetime.fromisoformat(proto_user.updated_at) if proto_user.updated_at else None,
            created_at=datetime.fromisoformat(proto_user.created_at),
        )
```

**user_token_pb2.py**
```python
import user_token_pb2
from models import UserTokenModel
from uuid import UUID
from datetime import datetime

class UserTokenProtoConverter:
    @staticmethod
    def user_token_to_proto(user_token: UserTokenModel) -> user_token_pb2.UserToken:
        return user_token_pb2.UserToken(
            id=str(user_token.id),
            user_id=str(user_token.user_id),
            token=user_token.token,
            created_at=user_token.created_at.isoformat(),
            expired_at=user_token.expired_at.isoformat(),
        )

    @staticmethod
    def proto_to_user_token(proto_user_token: user_token_pb2.UserToken) -> UserTokenModel:
        return UserTokenModel(
            id=UUID(proto_user_token.id),
            user_id=UUID(proto_user_token.user_id),
            token=proto_user_token.token,
            created_at=datetime.fromisoformat(proto_user_token.created_at),
            expired_at=datetime.fromisoformat(proto_user_token.expired_at),
        )
```

With these steps, you can create `.proto` files, generate the corresponding Python code, and implement conversion functions for all your models. Make sure to adjust the imports and paths according to your project's structure.