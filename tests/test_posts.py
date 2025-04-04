from app import schemas
import pytest


def test_get_all_posts(auth_client, post_create):
    resp = auth_client.get("/posts/")

    def validate_posts(post):
        return schemas.PostOut(**post)

    posts = map(validate_posts, resp.json())

    assert len(resp.json()) == len(post_create)
    assert resp.status_code == 200


def test_not_auth_user(client):
    resp = client.get("/posts/")
    assert resp.status_code == 401


def test_get_not_existing_post(auth_client):
    resp = auth_client.get("/posts/0")
    assert resp.status_code == 404


def test_get_one_post(auth_client, post_create):
    resp = auth_client.get(f"/posts/{post_create[0].id}")

    post = schemas.PostOut(**resp.json())

    assert resp.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("hello", "what's up", True),
        ("Hey", "bro", False),
        ("Nothing special", "hehehe", True),
    ],
)
def test_create_post(auth_client, title, content, published):
    resp = auth_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post2(**resp.json())
    assert resp.status_code == 201


def test_delete_post(auth_client, post_create):
    resp = auth_client.delete(f"/posts/{post_create[0].id}")

    assert resp.status_code == 204


def test_not_auth_delete_post(client, post_create):
    resp = client.delete(f"/posts/{post_create[0].id}")

    assert resp.status_code == 401


def test_delete_post_not_exist(auth_client, post_create):
    resp = auth_client.delete("/posts/0")
    assert resp.status_code == 404


def test_delete_other_user_post(auth_client, post_create):
    resp = auth_client.delete(f"/posts/{post_create[3].id}")
    assert resp.status_code == 403


def test_update_post(auth_client, post_create):
    resp = auth_client.put(
        f"/posts/{post_create[0].id}",
        json={"title": "new title", "content": "new content", "published": False}
    )
    assert resp.status_code == 200

def test_update_not_auth_post(client, post_create):
    resp = client.put(
        f"/posts/{post_create[0].id}",
        json={"title": "new title", "content": "new content", "published": True}
    )
    assert resp.status_code == 401

def test_update_other_user_post(auth_client, post_create):
    resp = auth_client.put(
        f"/posts/{post_create[3].id}",
        json={"title": "new title", "content": "new content", "published": True}
    )
    assert resp.status_code == 403

def test_update_post_not_exist(auth_client, post_create):
    resp = auth_client.put("/posts/0", json={"title": "new title", "content": "new content", "published": True})
    assert resp.status_code == 404