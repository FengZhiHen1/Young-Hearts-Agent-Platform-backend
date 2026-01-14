import uuid
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def register_user(username, password, roles=None):
    payload = {
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
        "gender": "male",
        "nickname": "Test User",
    }
    if roles:
        payload["roles"] = roles
    r = client.post("/users/register", json=payload)
    assert r.status_code == 201, r.text
    return r.json()

def login_user(username, password, use_cookie=False):
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()
    session_id = data.get("session_id")
    # Web端用cookie
    if use_cookie:
        cookies = r.cookies
        return session_id, cookies
    # App端用header
    return session_id, {"X-Session-ID": session_id}

def logout_user(session_id=None, cookies=None):
    if cookies:
        r = client.post("/auth/logout", cookies=cookies)
    elif session_id:
        r = client.post("/auth/logout", headers={"X-Session-ID": session_id})
    else:
        r = client.post("/auth/logout")
    assert r.status_code == 200, r.text

def get_me(headers=None, cookies=None):
    if cookies:
        r = client.get("/users/me", cookies=cookies)
    elif headers:
        r = client.get("/users/me", headers=headers)
    else:
        r = client.get("/users/me")
    return r

def test_register_login_logout_web_and_app():
    username = f"webappuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"
    # 注册
    register_user(username, password)
    # Web端登录（cookie）
    session_id_web, cookies = login_user(username, password, use_cookie=True)
    r = get_me(cookies=cookies)
    assert r.status_code == 200
    assert r.json()["username"] == username
    # App端登录（header）
    session_id_app, headers = login_user(username, password, use_cookie=False)
    r2 = get_me(headers=headers)
    assert r2.status_code == 200
    assert r2.json()["username"] == username
    # 登出后会话失效
    logout_user(session_id=session_id_app)
    r3 = get_me(headers=headers)
    assert r3.status_code == 401
    logout_user(cookies=cookies)
    r4 = get_me(cookies=cookies)
    assert r4.status_code == 401

def test_role_permission_and_sensitive_field():
    # 注册多角色用户
    username = f"roleuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"
    roles = ["user", "expert"]
    register_user(username, password, roles=roles)
    session_id, headers = login_user(username, password)
    # 访问需要 expert 角色的接口
    r = client.get("/protected/expert", headers=headers)
    assert r.status_code == 200
    # 访问需要 volunteer 角色的接口应 403
    r2 = client.get("/protected/volunteer", headers=headers)
    assert r2.status_code == 403
    # 敏感字段脱敏校验（如有）
    # r3 = client.get("/users/me", headers=headers)
    # assert "sensitive_field" not in r3.json()  # 示例

def test_session_expiry():
    username = f"expireuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"
    register_user(username, password)
    session_id, headers = login_user(username, password)
    # 模拟会话过期（假设有接口可强制失效）
    client.post("/debug/expire_session", headers=headers)
    r = get_me(headers=headers)
    assert r.status_code == 401

def test_register_duplicate():
    username = f"dupuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"
    register_user(username, password)
    r = client.post("/users/register", json={
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
        "gender": "male",
        "nickname": "Test User",
    })
    assert r.status_code in (400, 409)
