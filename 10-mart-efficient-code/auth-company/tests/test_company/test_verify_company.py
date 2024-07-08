# from starlette.testclient import TestClient
# from app.models.all_models import CompanyModel
# # from app.config.settings import TEST_DATABASE_URL
# from app.config.security import hashed_password, hashed_url
# import json
# import time
# from sqlmodel import Session
# from fastapi import status
# from datetime import datetime, timezone

# NAME="xyz"
# EMAIL="xyz@xyz.com"
# PASSWORD="Abcdef1@"
# DESCRIPTION="This is the company that provide bueaty product"

# def test_verify_new_company_with_valid_email_token(client:TestClient, unverified_company):
#     token = hashed_url(unverified_company.get_context_str())
#     json_data = { "email": unverified_company.email, "token": token}
#     res = client.post("/company/verify-company-account", json=json_data)
#     assert res.status_code == 200
#     assert res.json() == {"status": status.HTTP_200_OK, "message": f"This company {NAME} have succcessfully verified, please visit to login"}

# def test_verify_new_company_with_invalid_email(client:TestClient, unverified_company):
#     token = hashed_url(unverified_company.get_context_str())
#     json_data = { "email": "wxyz@wxyz.com", "token": token}
#     res = client.post("/company/verify-company-account", json=json_data)
#     assert res.status_code == 400
#     assert res.json() == {"detail": "Invalid creadential"}

# def test_verify_new_company_with_invalid_token(client:TestClient, unverified_company):
#     token = hashed_url(unverified_company.get_context_str("qwert")) # token invalid
#     json_data = { "email": unverified_company.email, "token": token}
#     res = client.post("/company/verify-company-account", json=json_data)
#     assert res.status_code == 401
#     assert res.json() == {"detail": "Token eigther is invalid or expired"}

# def test_verified_new_company_trying_to_verify_again(client:TestClient, verified_company):
#     token = hashed_url(verified_company.get_context_str()) 
#     json_data = { "email": verified_company.email, "token": token}
#     res = client.post("/company/verify-company-account", json=json_data)
#     assert res.status_code == 200
#     assert res.json() == {"message": f"Company '{NAME}' has already verified, please login it"}

# # def test_verify_new_company_with_existing_email(client:TestClient, test_session: Session):
# #     hash_password = hashed_password(PASSWORD)
# #     company = CompanyModel(email=EMAIL, name=NAME, password=hash_password, description=DESCRIPTION, updated_at=datetime.now(timezone.utc))
# #     token = hashed_url(company.get_context_str())
# #     company_dict = { "id": str(company.id),
# #     "name": company.name,
# #     "description": company.description, 
# #     "email": company.email,
# #     "password": company.password,
# #     "is_verified": company.is_verified,
# #     "verified_at": None,
# #     "created_at": company.created_at.isoformat() if company.updated_at else "",
# #     "updated_at": company.updated_at.isoformat() if company.updated_at else "" }
# #     # company_json_data = json.dumps(company_dict).encode("utf-8")
# #     company_res = client.post("/company/register", json=company_dict)
# #     assert company_res.status_code == 201
# #     time.sleep(2)
# #     json_data = { "email": EMAIL, "token": token}
# #     res = client.post("/company/verify-company-account", json=json_data)
# #     assert res.status_code == 400
# #     assert res.json() == {"detail": "Invalid creadential"}
#     # assert res.json() == {"status": status.HTTP_200_OK, "message": f"This company {NAME} have succcessfully verified, please visit to login"}

# # def test_verify_new_company_with_invalid_email(client:TestClient, unverified_company):
# #     hash_password = hashed_password(PASSWORD)
# #     company = CompanyModel(email="xyz@xyz.com", name=NAME, password=hash_password, description=DESCRIPTION)
# #     token = hashed_url(company.get_context_str())
# #     json_data = { "email": EMAIL, "token": token}
# #     res = client.post("/company/verify-company-account", json=json_data)
# #     assert res.status_code == 200
# #     assert res.json() == {"status": status.HTTP_200_OK, "message": f"This company {NAME} have succcessfully verified, please visit to login"}

# # status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid creadential"