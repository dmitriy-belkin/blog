from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserCreate, User
from models import User as UserModel
from database import get_db
from auth import get_password_hash

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user_create.password)
    new_user = UserModel(
        username=user_create.username,
        full_name=user_create.full_name,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
