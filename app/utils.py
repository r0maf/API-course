from passlib.context import CryptContext
from fastapi import HTTPException
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_hash_check(password, hashed_password):
    boolean = pwd_context.verify(password, hashed_password)
    
    if not boolean:
        raise HTTPException(status_code=401, detail="Invalid password")
    return boolean

def hash(password):
    return pwd_context.hash(password)