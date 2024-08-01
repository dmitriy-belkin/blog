from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_password_hash
from schemas import User, UserCreate
from models import User as UserModel
from database import get_db

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
