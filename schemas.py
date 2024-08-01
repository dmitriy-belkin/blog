from pydantic import BaseModel, EmailStr, constr, Field, field_validator
from typing import Optional
import re


class UserBase(BaseModel):
    username: Optional[str] = Field(None, title="Username", description="Optional username for the user")
    email: EmailStr = Field(..., title="Email", description="User email address, required")
    full_name: Optional[str] = Field(None, title="Full Name", description="Optional full name of the user")


class UserCreate(UserBase):
    password: constr(min_length=8) = Field(...,
                                           title="Пароль",
                                           description="Password must be at least 8 characters long and include at "
                                                       "least one uppercase letter, one lowercase letter, one number, "
                                                       "and one special character")

    @field_validator('password')
    def validate_password(cls, v):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, v):
            raise ValueError(
                'Пароль должен содержать минимум 8 символов, одну заглавную букву, '
                'одну строчную букву, одну цифру и один специальный символ'
            )
        return v


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
