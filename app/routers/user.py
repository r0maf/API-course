from .. import models, schemas, utils
from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# можно реализовать номер телефона, восстановление пароля, смс и тд и тп
@router.get("/", response_model=schemas.User)
def get_user(pwd: str, email: schemas.EmailStr, db: Session = Depends(get_db)):
    if email:
        user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    if utils.password_hash_check(pwd, user.password):
        user.password = pwd
        return user


@router.delete("/", status_code=204)
def delete_user(pwd: str, email: schemas.EmailStr, db: Session = Depends(get_db)):
    if email:
        user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")
    if utils.password_hash_check(pwd, user.password):
        db.delete(user)
        db.commit()
        return Response(status_code=204)


@router.put("/", response_model=schemas.User)
def update_user(
    pwd: str,
    email: schemas.EmailStr,
    body: schemas.CreateUser,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == email).first()
    b_pwd = body.password
    if not user:
        raise HTTPException(status_code=404, detail="Sorry, your element doesn't exist")

    if not utils.password_hash_check(pwd, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    body.password = utils.hash(body.password)

    user_query = db.query(models.User).filter(models.User.email == email)
    user_query.update(body.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    user.password = b_pwd
    return user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput
)
def create_user(body: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash(body.password)
        body.password = hashed_password

        new_user = models.User(**body.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=404, detail="an email already exists")
