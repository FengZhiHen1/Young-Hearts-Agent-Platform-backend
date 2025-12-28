import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_and_get_me():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"

    # register
    r = client.post("/users/register", json={
        "username": username,
        "password": password,
        "email": "test@example.com",
        "full_name": "Test User",
    })
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["username"] == username

    # login using form (OAuth2 password flow)
    r2 = client.post("/auth/token", data={"username": username, "password": password})
    assert r2.status_code == 200, r2.text
    token_data = r2.json()
    assert token_data.get("token_type") == "bearer"
    access_token = token_data.get("access_token")
    assert access_token

    # get current user
    r3 = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert r3.status_code == 200, r3.text
    me = r3.json()
    assert me["username"] == username

    # cleanup - delete user
    r4 = client.delete("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert r4.status_code == 204, r4.text
