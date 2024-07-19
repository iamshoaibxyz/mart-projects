from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

DATABASE_URL=os.environ.get("DATABASE_URL","")
# TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
ORDER_BACKEND_HOST = os.environ.get("ORDER_BACKEND_HOST","http://127.0.0.1:8001")

SECRET_TOKEN=os.environ.get("SECRET_TOKEN","qwert123")
TOKEN_EXPIRY=os.environ.get("TOKEN_EXPIRY" ,15)
REFRESH_TOKEN_EXPIRY=os.environ.get("REFRESH_TOKEN_EXPIRY" ,1) # day
TOKEN_ALGROITHM=os.environ.get("TOKEN_ALGROITHM" ,"HS256")