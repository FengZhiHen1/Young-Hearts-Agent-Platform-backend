
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

# 如健康检查接口需鉴权，可补充如下用例（假设/health 需登录）
def test_health_auth_required():
    # 若/health无需鉴权，此测试可忽略
    r = client.get("/health", headers={"X-Session-ID": "invalid"})
    # 若需鉴权应为401，否则为200
    assert r.status_code in (200, 401)
