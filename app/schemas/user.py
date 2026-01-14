from typing import Optional
from pydantic import BaseModel



# 登录用 Pydantic 模型
class UserLogin(BaseModel):
    username: str
    password: str



class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    roles: Optional[list[str]] = []
    status: Optional[str] = "active"
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False



class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    roles: Optional[list[str]] = []
    status: Optional[str] = "active"



class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# Session Pydantic 模型
from datetime import datetime

class SessionBase(BaseModel):
    session_id: str
    user_id: int
    created_at: datetime
    expired_at: Optional[datetime] = None
    user_agent: Optional[str] = None
    ip: Optional[str] = None

class SessionCreate(BaseModel):
    user_id: int
    expired_at: Optional[datetime] = None
    user_agent: Optional[str] = None
    ip: Optional[str] = None

class SessionOut(SessionBase):
    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
