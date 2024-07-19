from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

INVENTORY_DATABASE_URL=os.environ.get("INVENTORY_DATABASE_URL")
# TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
INVENTORY_BACKEND_HOST = os.environ.get("INVENTORY_BACKEND_HOST")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
TOKEN_ALGROITHM = os.environ.get("TOKEN_ALGROITHM")

