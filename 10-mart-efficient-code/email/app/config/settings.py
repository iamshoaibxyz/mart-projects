from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

# USER_DATABASE_URL=os.environ.get("DATABASE_URL","postgresql://shoaib:mypassword@postgresContainer:5432/mydatabase")
# TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
ORDER_BACKEND_HOST = os.environ.get("ORDER_BACKEND_HOST","http://127.0.0.1:8003")

SECRET_TOKEN=os.environ.get("SECRET_TOKEN","qwert123")
TOKEN_EXPIRY=os.environ.get("TOKEN_EXPIRY" ,5)
TOKEN_ALGROITHM=os.environ.get("TOKEN_ALGROITHM" ,"HS256")