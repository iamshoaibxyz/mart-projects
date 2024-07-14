from dotenv import load_dotenv, find_dotenv

import os

_ = load_dotenv(find_dotenv())

DATABASE_URL=os.environ.get("DATABASE_URL","postgresql://shoaib:mypassword@postgresContainer:5432/mydatabase")
# TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
ORDER_BACKEND_HOST = os.environ.get("ORDER_BACKEND_HOST","http://127.0.0.1:8007")

STRIPE_API_KEY='sk_test_51PQwQtIf22jmWnXxgTSFMFUHxW75nkwV9kwyT6g1U62kxv65cneW5XUs0QbLbVAkB4RmBf9lh7SOB5nDC0apqWsL00DyRI6fF2'
