from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

DATABASE_URL=os.environ.get("DATABASE_URL","postgresql://shoaib:mypassword@postgresContainer:5432/mydatabase")
# TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
ORDER_BACKEND_HOST = os.environ.get("ORDER_BACKEND_HOST","http://127.0.0.1:8004")