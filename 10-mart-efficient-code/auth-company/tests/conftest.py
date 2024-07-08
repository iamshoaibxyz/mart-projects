from sqlmodel import create_engine, Session, SQLModel
from starlette.testclient import TestClient 
import pytest
from app.main import app
from datetime import datetime, timezone
from app.config.database import get_session
from app.models.all_models import CompanyModel
from app.config.settings import TEST_DATABASE_URL
from app.config.security import hashed_password

connection_str = str(TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str, )


NAME="xyz"
EMAIL="xyz@xyz.com"
PASSWORD="Abcdef1@"
DESCRIPTION="This is the company that provide bueaty product"

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

@pytest.fixture(scope="function")
def unverified_company(test_session: Session):
    company = CompanyModel(email=EMAIL, name= NAME, description= DESCRIPTION, password= hashed_password(PASSWORD))
    test_session.add(company)
    test_session.commit()
    test_session.refresh(company)
    return company

@pytest.fixture(scope="function")
def verified_company(test_session: Session):
    company = CompanyModel(
        email=EMAIL, name= NAME, 
        description= DESCRIPTION, 
        password= hashed_password(PASSWORD), 
        is_verified=True, 
        verified_at=datetime.now(timezone.utc))
    
    test_session.add(company)
    test_session.commit()
    test_session.refresh(company)
    return company