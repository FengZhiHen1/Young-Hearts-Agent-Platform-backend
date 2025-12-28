from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserOut(UserBase):
    id: int

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
