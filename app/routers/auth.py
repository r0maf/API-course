from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2, schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if user_credentials.username == "":
        raise HTTPException(status_code=422, detail="Invalid Credentials")
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    if utils.password_hash_check(user_credentials.password, user.password):
        
        access_token = oauth2.create_access_token(data = {"user_id": user.id})
        
        return {"access_token": access_token, "token_type": "bearer"}
        