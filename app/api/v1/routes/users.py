from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import create_user, get_user_by_username, update_user, delete_user
from app.services.auth import get_current_user_from_context as get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="用户名或邮箱已存在")



# 仅允许登录用户访问，示例：普通用户和志愿者均可
@router.get("/me", response_model=UserOut)
@require_roles(["user", "volunteer", "expert", "admin"])
async def read_users_me(current_user=Depends(get_current_user)):
    # 敏感字段按角色脱敏示例
    user_dict = current_user.dict() if hasattr(current_user, 'dict') else dict(current_user)
    # 性别字段直接返回，无需脱敏
    # 假设手机号为敏感字段，仅 admin/专家可见
    if "admin" not in current_user.roles and "expert" not in current_user.roles:
        user_dict.pop("phone", None)
    return user_dict



# 仅允许本人或管理员修改
@router.put("/me", response_model=UserOut)
@require_roles(["user", "admin"])
async def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = payload.dict(exclude_unset=True)
    if "password" in data:
        data.pop("password")
    user = update_user(db, current_user, data)
    return user



# 仅允许本人或管理员注销
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["user", "admin"])
async def delete_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_user(db, current_user)
    return None
