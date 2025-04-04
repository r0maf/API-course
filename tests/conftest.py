from app import schemas
from app.config import settings as ss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from app import models
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token

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

@pytest.fixture
def test_user2(client):
    user_data = {"email": "frolov@gmail.com", "password": "frolov"}
    resp = client.post("/users/", json=user_data)
    assert resp.status_code == 201
    new_user = resp.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(client, test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def post_create(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts