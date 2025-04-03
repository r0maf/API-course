from app.config import settings as ss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{ss.db_username}:{ss.db_password}@{ss.db_hostname}:{ss.db_port}/{ss.db_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "roma@gmail.com", "password": "roma"}
    resp = client.post("/users/", json=user_data)
    assert resp.status_code == 201
    new_user = resp.json()
    new_user["password"] = user_data["password"]
    return new_user