from sqlmodel import create_engine, Session, SQLModel
from starlette.testclient import TestClient 
import pytest
from app.main import app
from datetime import datetime, timezone
from app.config.database import get_session
from app.models.all_models import CompanyModel, UserModel
from app.config.settings import TEST_DATABASE_URL
from app.config.security import hashed_password

connection_str = str(TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str, )


F_NAME="abc"
L_NAME="xyz"
EMAIL="abc@xyz.com"
PASSWORD="Abcdef1@"

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
def unverified_user(test_session: Session):
    user = UserModel(email=EMAIL, first_name= F_NAME, last_name=L_NAME, password= hashed_password(PASSWORD))
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def verified_user(test_session: Session):
    user = UserModel(
        email=EMAIL, 
        first_name= F_NAME, 
        last_name=L_NAME, 
        password= hashed_password(PASSWORD), 
        is_verified=True, 
        verified_at=datetime.now(timezone.utc))
    
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user