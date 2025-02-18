from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).one()
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="we cannot find your post")


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )
    db.add(new_post)
    db.commit()
    return {"message": "your post was successfully created"}


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).one()
    if post:
        db.delete(post)
        db.commit()
        yield Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")


@app.put("/posts/{id}")
def update_post(id: int, body: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).one()
    if post:
        post.title = body.title
        post.content = body.content
        post.published = body.published
        db.commit()
        return {
            "information": {
                "message": "The post was successfully updated",
                "updated_post": post,
            }
        }
    else:
        raise HTTPException(status_code=404, detail="sorry, the id doesn't exist")
