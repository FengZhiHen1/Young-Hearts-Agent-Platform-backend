from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import create_user, get_user_by_username, update_user, delete_user
from app.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="用户名或邮箱已存在")


@router.get("/me", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = payload.dict(exclude_unset=True)
    if "password" in data:
        # password will be handled in user_service if needed; for now remove plain password
        data.pop("password")
    user = update_user(db, current_user, data)
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_user(db, current_user)
    return None
