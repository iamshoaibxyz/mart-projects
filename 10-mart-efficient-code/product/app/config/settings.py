from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

PRODUCT_DATABASE_URL=os.environ.get("PRODUCT_DATABASE_URL")
PRODUCT_BACKEND_HOST = os.environ.get("PRODUCT_BACKEND_HOST","http://127.0.0.1:8004")

SECRET_TOKEN=os.environ.get("SECRET_TOKEN")
TOKEN_ALGROITHM=os.environ.get("TOKEN_ALGROITHM")
