from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base


# 用户主表
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    gender: Mapped[str] = mapped_column(String(16), default="hidden")  # ['male', 'female', 'hidden']
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(512))
    roles: Mapped[str] = mapped_column(String(255), nullable=False, default='[]')  # JSON 字符串数组
    status: Mapped[str] = mapped_column(String(32), default="active")  # ['active', 'banned', 'pending_review']
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())


# 志愿者扩展表
class VolunteerProfile(Base):
    __tablename__ = "volunteer_profiles"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(32))
    public_email: Mapped[str] = mapped_column(String(320))
    is_public_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    service_hours: Mapped[str] = mapped_column(String(32), default="0")
    skills: Mapped[str] = mapped_column(String(255), default='[]')  # JSON 字符串数组
    status: Mapped[str] = mapped_column(String(32), default="pending")  # ['pending', 'approved', 'rejected']
    work_status: Mapped[str] = mapped_column(String(32), default="offline")  # ['online', 'busy', 'offline']


# 专家扩展表
class ExpertProfile(Base):
    __tablename__ = "expert_profiles"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(32))
    public_email: Mapped[str] = mapped_column(String(320))
    title: Mapped[str] = mapped_column(String(255))
    org: Mapped[str] = mapped_column(String(255))
    skills: Mapped[str] = mapped_column(String(255), default='[]')  # JSON 字符串数组
    status: Mapped[str] = mapped_column(String(32), default="pending")


# Session 会话表
class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    user_agent: Mapped[str] = mapped_column(String(255))
    ip: Mapped[str] = mapped_column(String(64))
