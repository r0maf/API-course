from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:   
        orm_mode = True
        
class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class User(UserOutput):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None