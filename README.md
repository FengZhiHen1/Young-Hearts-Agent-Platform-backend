
# 心青年智能体平台 — Backend (FastAPI)

这是项目后端（FastAPI）服务的代码仓库，包含基础的应用入口、配置、数据库会话以及用户管理与知识库占位实现。

## 快速开始（Windows PowerShell）

```powershell
# 在项目根创建并激活虚拟环境
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（使用 app/core/config.py 中的 DATABASE_URL）
python -c "from app.db.session import init_db; init_db()"

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 运行测试

建议在激活虚拟环境后运行：

```powershell
# 激活虚拟环境
. .\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
pytest tests/test_users.py -q
```

或运行全部测试：

```powershell
pytest tests/ -q
```

## 用户管理（参考实现与验证）

本仓库实现了基本的用户注册、登录（OAuth2 password + JWT）与当前用户查询接口。以下是快速验证示例：

- 注册：

```bash
curl -X POST "http://127.0.0.1:8000/users/register" -H "Content-Type: application/json" -d \
'{"username":"alice","email":"alice@example.com","password":"secret"}'
```

- 获取 token（登录）：

```bash
curl -X POST "http://127.0.0.1:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d \
'grant_type=&username=alice&password=secret&scope=&client_id=&client_secret='
```

返回示例：

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

- 使用 token 访问受保护接口 `GET /users/me`：

```bash
curl -H "Authorization: Bearer <JWT>" http://127.0.0.1:8000/users/me
```

## 主要文件

- `app/main.py`：FastAPI 应用入口与路由注册
- `app/core/config.py`：配置（从环境变量读取）
- `app/db/session.py`：SQLAlchemy session 与 `init_db()` 函数
- `app/models/`：ORM 模型（包含 `User`）
- `app/schemas/`：Pydantic 模型
- `app/services/`：业务逻辑（认证、用户 CRUD）

