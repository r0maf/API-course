def test_vote(auth_client, post_create):
    resp = auth_client.post("/vote/", json={"post_id": post_create[3].id, "dir": 1})
    assert resp.status_code == 201

def test_unvote(auth_client, post_create, vote_create):
    resp = auth_client.post("/vote/", json={"post_id": post_create[3].id, "dir": 0})
    assert resp.status_code == 201

def test_vote_twice_post(auth_client, post_create, vote_create):
    resp = auth_client.post("/vote/", json={"post_id": post_create[3].id, "dir": 1})
    assert resp.status_code == 409

def test_vote_delete_non_exist(auth_client, post_create):
    resp = auth_client.post("/vote/", json={"post_id": post_create[3].id, "dir": 0})
    assert resp.status_code == 404

def test_vote_non_exist(auth_client, post_create):
    resp = auth_client.post("/vote/", json={"post_id": 0, "dir": 1})
    assert resp.status_code == 404

def test_unauth_vote(client, post_create):
    resp = client.post("/vote/", json={"post_id": post_create[3].id, "dir": 1})
    assert resp.status_code == 401