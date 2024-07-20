from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

ORDER_DATABASE_URL=os.environ.get("ORDER_DATABASE_URL","postgresql://shoaib:mypassword@postgresContainer:5432/mydatabase")
ORDER_BACKEND_HOST = os.environ.get("ORDER_BACKEND_HOST","http://127.0.0.1:8005")

SECRET_TOKEN=os.environ.get("SECRET_TOKEN")
TOKEN_ALGROITHM=os.environ.get("TOKEN_ALGROITHM")