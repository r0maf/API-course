from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    return post


@router.get("/", response_model=list[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=204)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    db.delete(post)
    db.commit()
    return Response(status_code=204)


@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, body: schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    post_query.update(body.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
