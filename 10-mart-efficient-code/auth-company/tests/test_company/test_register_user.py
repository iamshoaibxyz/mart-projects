# from starlette.testclient import TestClient
# from fastapi import status

# NAME="xyz"
# EMAIL="xyz@xyz.com"
# PASSWORD="Abcdef1@"
# DESCRIPTION="This is the company that provide bueaty product"


# def test_register_new_company(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": PASSWORD }
#     res = client.post("/company/register", json=json_data)    
#     assert res.status_code == 201
#     assert res.json() == {"status": status.HTTP_201_CREATED, "message": "you have succcessfully signed up the company and we have send you an email, please check and verify"}

# def test_register_new_company_with_existing_email(client:TestClient, unverified_company):
#     json_data = { "email": EMAIL, "name": "abcdef", "description": DESCRIPTION, "password": PASSWORD }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 406
#     assert res.json() == {"detail":f"with this email '{EMAIL}', Company is  already registerd, please use different email to register new company"}

# def test_register_new_company_with_existing_name(client:TestClient, unverified_company):
#     json_data = { "email": "wxyz@wxyz.com", "name": NAME, "description": DESCRIPTION, "password": PASSWORD }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 406
#     assert res.json() == { "detail": f"with this Company name '{NAME}', Company is already registerd, please use different name"}

# def test_register_new_unverified_company_with_existing_name_and_email(client:TestClient, unverified_company):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": PASSWORD }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 406
#     assert res.json() == { "detail": f"Company '{NAME}' is already registered but not verified, we have send you an email, please check and verify to your company"}

# def test_register_new_verified_company_with_existing_name_and_email(client:TestClient, verified_company):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": PASSWORD }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 201
#     assert res.json() == { "message": f"Company '{NAME}' is already registered and verified, please visit to login page, and login to your company"}

# def test_register_new_company_with_small_password(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": "abc123" }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == { "detail": "Password must be at least 8 characters long"}

# def test_register_new_company_without_uppercase_letter(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": "abc12345@" }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == { "detail": "Password must contain at least one uppercase letter"}

# def test_register_new_company_without_lowercase_letter(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": "ABC12345@" }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == { "detail": "Password must contain at least one lowercase letter"}

# def test_register_new_company_without_digit(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": "ABCdefgh@" }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == { "detail": "Password must contain at least one digit"}

# def test_register_new_company_without_special_character(client:TestClient):
#     json_data = { "email": EMAIL, "name": NAME, "description": DESCRIPTION, "password": "ABCdefgh12" }
#     res = client.post("/company/register", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == { "detail": "Password must contain at least one special character"}

