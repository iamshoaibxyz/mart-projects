import pytest
from starlette.testclient import TestClient 
from sqlmodel import create_engine, Session, SQLModel
from app.models.all_models import CompanyModel
from app.main import app
from app.config.settings import TEST_DATABASE_URL
from app.config.database import get_session
from app.config.security import hashed_password, verify_hashed_password, hashed_url, verify_hashed_url

connection_str = str(TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str, )

@pytest.fixture(scope="function")
def test_session():
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def app_test():
    SQLModel.metadata.create_all(engine)
    yield app
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass
    app_test.dependency_overrides[get_session] = _test_db
    return TestClient(app_test)
