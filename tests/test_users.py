from app import schemas
from app.oauth2 import jwt, SECRET_KEY, ALGORITHM


def test_user_create(client):
    resp = client.post("/users/", json={"email": "roma@gmail.com", "password": "roma"})
    assert resp.status_code == 201

def test_user_login(client, test_user):
    resp = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_token = schemas.Token(**resp.json())
    payload = jwt.decode(login_token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_token.token_type == "bearer"
    assert resp.status_code == 200