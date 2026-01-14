
from fastapi import APIRouter, Request, Response, status, HTTPException
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

# 登录接口：成功后写 session 表，Web 端 set_cookie，App 端返回 session_id
@router.post("/login", response_model=UserOut)
async def login(user_in: UserLogin, response: Response, request: Request):
    user, session_id = await auth_service.login(user_in, request)
    user_agent = request.headers.get("user-agent", "")
    # 简单判断：web端用cookie，app端返回session_id
    if "web" in user_agent.lower():
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return user
    else:
        return {"user": user, "session_id": session_id}

# 登出接口：清理 session 表记录，清除 Cookie/Header
@router.post("/logout")
async def logout(request: Request, response: Response):
    await auth_service.logout(request)
    user_agent = request.headers.get("user-agent", "")
    if "web" in user_agent.lower():
        response.delete_cookie(key="session_id")
    return {"msg": "logout success"}

# 注册接口：字段与校验对齐 API 设计
@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate):
    user = await auth_service.register(user_in)
    return user
