# 心青年智能体平台 — Backend (FastAPI)

这是根据项目结构文档生成的初始后端骨架。包含最小的 FastAPI 入口、配置与数据库会话占位实现，以及知识库模块的占位文件。

快速开始（在 Windows PowerShell 中）：

```powershell
# 建议先创建并激活虚拟环境
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

主要文件：
- `app/main.py`：FastAPI 入口
- `app/core/config.py`：配置（读取 `.env`）
- `app/db/session.py`：SQLAlchemy session 与 `init_db()`
- `app/knowledge/`：知识库相关模块（占位）

接下来建议：
- 根据需要实现 `app/models` 中的实体并运行 `scripts/init_db.py`
- 实现向量存储适配器并完善 `app/knowledge` 中的检索/ingest/rag 实现
