# login-company
from starlette.testclient import TestClient
from app.models.all_models import CompanyModel
# from app.config.settings import TEST_DATABASE_URL
from app.config.security import hashed_password, hashed_url
import json
import time
from sqlmodel import Session
from fastapi import status
from datetime import datetime, timezone

NAME="xyz"
EMAIL="xyz@xyz.com"
PASSWORD="Abcdef1@"
DESCRIPTION="This is the company that provide bueaty product"

def test_login_company_with_valid_email_password(client:TestClient, verified_company):
    form_data = {
        "username": EMAIL,  # OAuth2PasswordRequestForm uses 'username' for email
        "password": PASSWORD,
    }
    res = client.post("/company/company-login", data=form_data)    
    assert res.status_code == 200
    response_data = res.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert "expires_in" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_company_with_invalid_email(client:TestClient, verified_company):
    form_data = {
        "username": "wxyz@wxyz.com",  # OAuth2PasswordRequestForm uses 'username' for email
        "password": PASSWORD,
    }
    res = client.post("/company/company-login", data=form_data)    
    assert res.status_code == 400
    assert res.json() == {"detail":f"Company with this email 'wxyz@wxyz.com'  is not registered here, please visit to signup and register to your company"}

def test_login_company_with_invalid_password(client:TestClient, verified_company):
    form_data = {
        "username": EMAIL,  # OAuth2PasswordRequestForm uses 'username' for email
        "password": "qwert123",
    }
    res = client.post("/company/company-login", data=form_data)    
    assert res.status_code == 401
    assert res.json() == {"detail":"Invalid creadential"}

def test_login_unverified_company_with(client:TestClient, unverified_company):
    form_data = {
        "username": EMAIL,  # OAuth2PasswordRequestForm uses 'username' for email
        "password": PASSWORD,
    }
    res = client.post("/company/company-login", data=form_data)    
    assert res.status_code == 400
    assert res.json() == {"detail": f"Company '{NAME}' is not verified, we have send you an email, please check and verify to your company"}
    
    