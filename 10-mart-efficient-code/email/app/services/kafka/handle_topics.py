
from app.utils.proto_conversion import proto_to_company_model, proto_to_user_model, proto_to_product_model, proto_to_inventory_transaction
from app.config.email import send_mail
from app.config.security import hashed_url
from app.utils.fetcher import fetch_company_detail_by_id, fetch_product_detail_by_id, fetch_stock_detail_by_id

# =================================user==================================

async def email_to_unverified_user(user_proto):
    user = proto_to_user_model(user_proto)
    context = str(user.get_context_str())
    hasded = hashed_url(context)
    email = user.email
    html = f"""
            token: {hasded} <br/>
            email: {email} <br/>
            This is the email for the old user verification.
            """
    await send_mail(email=email, html=html, subject="Verification")

async def email_to_new_user(user_proto): 
    user = proto_to_user_model(user_proto)
    context = str(user.get_context_str())
    hasded = hashed_url(context)
    email = user.email
    html = f"""
            token: {hasded} <br/>
            email: {email} <br/>
            This is the email for the new user verification.
            """
    await send_mail(email=email, html=html, subject="New User Verification")

async def email_to_new_verified_user(user_proto): 
    user = proto_to_user_model(user_proto)
    email = user.email
    html = f"""
            email: {email} <br/>
            Congratulation '{user.first_name} {user.last_name}' is successfully verified.
            """
    await send_mail(email=email, html=html, subject="User Verified")

async def email_to_reset_password_user(user_proto):
    user_model = proto_to_user_model(user_proto)
    verify_context = str(user_model.get_context_str())
    token_url = hashed_url(verify_context)
    email = user_model.email
    html = f"""
            token: {token_url} <br/>
            email: {email} <br/>
            This is the email for the reset password ... 
"""
    await send_mail(email=email, html=html, subject="Reset Password")

async def email_to_updated_password_user(user_proto):
    user_model = proto_to_user_model(user_proto)
    
    email = user_model.email
    html = f"""
            email: {email} <br />
            Your password has been successfully changed, now you should procied to the login
"""
    await send_mail(email=email, html=html, subject="Password Changed")

async def email_to_deleted_user(user_proto):
    user_model = proto_to_user_model(user_proto)
    
    email = user_model.email
    html = f"""
            email: {email} <br />
            You account {email} has been successfully deleted
"""
    await send_mail(email=email, html=html, subject="User deleted")


# =================================company==================================


async def email_to_new_company(company_proto):
    company = proto_to_company_model(company_proto)
    context = str(company.get_context_str())
    token = hashed_url(context)
    email = company.email
    name = company.name
    html = f"""
            email: {email} <br/>
            token: {token} <br/>
            {name.capitalize()} is successfully registered, copy the token and past it to reset-verify route
"""
    await send_mail(email=email, html=html, subject="Company Added")
    
async def verification_email_to_new_company(company_proto):
    company = proto_to_company_model(company_proto)
    email = company.email
    name = company.name
    html = f"""
            email: {email} <br/>
            Congratulation '{name.capitalize()}' is successfully verified
"""
    await send_mail(email=email, html=html, subject="Company Verified")
    
async def email_to_unverified_company(company_proto):
    company_model = proto_to_company_model(company_proto)
    url_context = company_model.get_context_str()
    token_url = hashed_url(url_context)
    email = company_model.email
    name = company_model.name
    html = f"""
            email: '{email}' <br/>
            token: '{token_url}' <br/>
            '{name.capitalize()}' was not verified, this token will help you to verify the company
"""
    await send_mail(email=email, html=html, subject="Verification")

async def email_to_reset_password_company(company_proto):
    company = proto_to_company_model(company_proto)
    verify_context = company.get_context_str("VERIFY_COMPANY_CONTEXT")
    token = hashed_url(verify_context)
    email = company.email
    html = f"""
            token: '{token}' <br/>
            email: '{email}' <br/>
            This is the email for the reset password, copy and past if on verify-reset route, and set new password to your company ... 
"""
    await send_mail(email=email, html=html, subject="Reset Password")

async def email_to_updated_company(company_proto):
    company = proto_to_company_model(company_proto)
    email = company.email
    html = f"""
            Email: '{email.lower()}' <br/>
            Name: '{company.name.lower()}' <br/>
            Description: '{company.description.lower()}' <br/>
            Here is the updated company detailed ...
"""
    await send_mail(email=email, html=html, subject="Updated company")

async def email_to_deleted_company(company_proto):
    company = proto_to_company_model(company_proto)
    email = company.email
    html = f"""
            Email: '{email.lower()}' <br/>
            Name: '{company.name.lower()}' <br/>
            Appologies  ...
"""
    await send_mail(email=email, html=html, subject="Deleted company")


# =================================product==================================

async def email_to_new_product_company(product_proto):
    product = proto_to_product_model(product_proto)
    company = await fetch_company_details_by_id(str(product.company_id)) 
    email = company.get("email")
    name = company.get("name")
    html = f"""
            Email: '{email}' <br/>
            Product: '{product.name}' <br/>
            Description: '{product.description}' <br/>
            Congratulation product '{product.name.capitalize()}' is successfully added by '{name.capitalize()}'  Company, please add inventory related detail"""
    await send_mail(email=email, html=html, subject="Product added")



# =================================inventory==================================

async def email_to_company_transaction_subtracted(transaction_proto):
    transaction = proto_to_inventory_transaction(transaction_proto)
    stock = await fetch_stock_detail_by_id(str(transaction.stock_id))
    product = await fetch_product_detail_by_id(str(stock.get("product_id")))
    company = await fetch_company_detail_by_id(str(product.get("company_id"))) 
    email = company.get("email")
    name = company.get("name")
    html = f"""
            Email: '{email}' <br/>
            Product: '{product.get("name")}' <br/>
            Description: '{product.description}' <br/>
            stock subtract: '{transaction.quantity}' <br/>
            current stock: '{stock.get("current_stock")}' <br/>
            Congratulation stock subtracted of '{product.get("name").capitalize()}' product, by '{name.capitalize()}'"""
    await send_mail(email=email, html=html, subject="Product added")

async def email_to_company_transaction_added(transaction_proto):
    transaction = proto_to_inventory_transaction(transaction_proto)
    stock = await fetch_stock_detail_by_id(str(transaction.stock_id))
    product = await fetch_product_detail_by_id(str(stock.get("product_id")))
    company = await fetch_company_detail_by_id(str(product.get("company_id"))) 
    email = company.get("email")
    name = company.get("name")
    html = f"""
            Email: '{email}' <br/>
            Product: '{product.get("name")}' <br/>
            Description: '{product.description}' <br/>
            stock added: '{transaction.quantity}' <br/>
            current stock: '{stock.get("current_stock")}' <br/>
            Congratulation stock add of '{product.get("name").capitalize()}' product, by '{name.capitalize()}'"""
    await send_mail(email=email, html=html, subject="Product added")


















# async def email_to_updated_product_company(product_proto):
#     product = proto_to_product(product_proto)
#     async with get_session() as session: 
#         company: CompanyModel = session.get(CompanyModel, product.company_id)
#         email = company.email
#         stock = session.exec(select(StockLevel).where(StockLevel.product_id==product.id)).first()
#         stock_content = (stock.current_stock if stock else "please add stock related detaild")
#         html = f"""
#                 email: '{email}'
#                 Congratulation product '{product.name.capitalize()}' is successfully updated by '{company.name.capitalize()}'  Company <br/> Product name: '{product.name.capitalize()}' <br/> Product Category: '{product.category.lower()}' <br/> Product price: '{product.price}' <br/> Current stock: {stock_content}  """
#         await send_mail(email=email, html=html)


# async def email_to_new_product_with_transaction(transaction_proto):
#     # transaction = proto_to_inventory_transaction(inventory_proto)
#     # product_id = transaction.product_id
#     async with get_session() as session:
#         transaction = session.get(InventoryTransaction, UUID(transaction_proto.transaction_id))
#         product = session.get(ProductModel, transaction.product_id)
#         company = session.get(CompanyModel, product.company_id)
#         email = company.email
#         html = f"""
#                 email: '{email}'
#                 Congratulation product '{product.name.capitalize()}' is successfully added by '{company.name.capitalize()}' <br/> Inventory:  '{transaction.quantity}' item  is also add <br/>"""
#         await send_mail(email=email, html=html)

