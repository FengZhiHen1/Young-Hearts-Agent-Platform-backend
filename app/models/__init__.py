from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 导入所有模型以便 metadata 注册
from app.models import user  # noqa: F401
