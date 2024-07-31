from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=8)


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: constr(min_length=1)
    content: str


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "owner_id": self.owner_id
        }
