from fastapi import FastAPI, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from . import utils
from .database import get_db, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

###############################################POSTS###############################################


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    return post


@app.get("/posts", response_model=list[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    db.delete(post)
    db.commit()
    return Response(status_code=204)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, body: schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    post_query.update(body.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


###############################################USERS###############################################


# можно реализовать номер телефона, восстановление пароля, смс и тд и тп
@app.get("/users/", response_model=schemas.User)
def get_user(pwd: str, email: schemas.EmailStr, db: Session = Depends(get_db)):
    if email:
        user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    if utils.password_hash_check(pwd, user.password):
        user.password = pwd
        return user



@app.delete("/users/", status_code=204)
def delete_user(pwd: str, email: schemas.EmailStr, db: Session = Depends(get_db)):
    if email:
        user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")
    if utils.password_hash_check(pwd, user.password):
        db.delete(user)
        db.commit()
        return Response(status_code=204)


@app.put("/users/", response_model=schemas.User)
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
    

@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput
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