from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes = True

class Post2(PostBase):
    id: int
    created_at: datetime
    owner_id: int


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserOutput

    class ConfigDict:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class ConfigDict:
        from_attributes = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class User(UserOutput):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0)]