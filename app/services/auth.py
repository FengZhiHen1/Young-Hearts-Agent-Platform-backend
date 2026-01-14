from datetime import datetime, timedelta, timezone
from typing import cast

from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.user_service import get_user_by_username, get_user_by_id
from app.db.session import get_db
from app.models.user import Session as SessionModel, User
import secrets

# 初始化密码加密上下文，指定用 bcrypt 算法，自动处理过时的加密方式
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 密码模式，指定 token URL（登录接口）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, cast(str, user.password_hash)):
        return None
    return user


# 登录：生成 session_id 并写入 session 表
async def login(user_in, request: Request):
    db: Session = next(get_db())
    user = get_user_by_username(db, user_in.username)
    if not user or not verify_password(user_in.password, getattr(user, "password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user_agent = request.headers.get("user-agent", "")
    ip = request.client.host if request.client else ""
    session_id = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    expired_at = now + timedelta(minutes=getattr(settings, "SESSION_EXPIRE_MINUTES", 10080))
    session = SessionModel(
        session_id=session_id,
        user_id=user.id,
        created_at=now,
        expired_at=expired_at,
        user_agent=user_agent,
        ip=ip
    )
    db.add(session)
    db.commit()
    return user, session_id

# 登出：清理 session 表记录，支持 Cookie/Header
async def logout(request: Request):
    db: Session = next(get_db())
    session_id = None
    if "session_id" in request.cookies:
        session_id = request.cookies["session_id"]
    elif "x-session-id" in request.headers:
        session_id = request.headers["x-session-id"]
    if session_id:
        db.query(SessionModel).filter(SessionModel.session_id == session_id).delete()
        db.commit()

# 注册：字段与校验对齐 API 设计
async def register(user_in):
    db: Session = next(get_db())
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = User(
        username=user_in.username,
        email=user_in.email,
        nickname=getattr(user_in, "nickname", None),
        avatar=getattr(user_in, "avatar", None),
        roles=str(user_in.roles) if user_in.roles else '[]',
        status=user_in.status or "active",
        is_active=True,
        password_hash=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 自动识别 Cookie/Header，查 session 表，注入 user
def get_current_user_from_context(request: Request, db: Session = Depends(get_db)):
    session_id = None
    # 优先 Cookie
    if settings.SESSION_COOKIE_NAME in request.cookies:
        session_id = request.cookies[settings.SESSION_COOKIE_NAME]
    # 其次 Header
    elif request.headers.get("X-Session-ID"):
        session_id = request.headers.get("X-Session-ID")
    if not session_id:
        raise HTTPException(status_code=401, detail="SessionID required")
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    # session.expired_at 需为 datetime 实例
    expired_at = getattr(session, "expired_at", None)
    if expired_at is not None and isinstance(expired_at, datetime):
        now = datetime.now(timezone.utc)
        if expired_at < now:
            raise HTTPException(status_code=401, detail="Session expired or invalid")
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found for session")
    return user
