from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from auth import get_password_hash
from schemas import User, UserCreate
from models import User as UserModel
from database import get_db

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    """
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    new_user = UserModel(
        username=username,
        full_name=full_name,
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
