from typing import Optional
from fastapi import HTTPException, Query, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{id}", response_model=schemas.Post)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    return post


@router.get("/", response_model=list[schemas.Post])
def get_all_posts(
    db: Session = Depends(get_db),
    my_posts: bool = Query(False),
    limit: Optional[int] = None,
    skip: int = 0,
    search: Optional[str] = "",
    current_user: dict = Depends(oauth2.get_current_user),
):
    if my_posts:
        posts = (
            db.query(models.Post)
            .filter(
                models.Post.user_id == current_user.id,
                models.Post.title.contains(search),
            )
            .limit(limit)
            .offset(skip)
            .all()
        )
    else:
        posts = (
            db.query(models.Post)
            .filter(models.Post.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = post.model_dump()
    post["user_id"] = current_user.id
    new_post = models.Post(**post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=204)
def delete_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not current_user.id == post.user_id:
        raise HTTPException(status_code=403, detail="it isn't your post")

    if not post:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    db.delete(post)
    db.commit()
    return Response(status_code=204)


@router.put("/{id}", response_model=schemas.Post)
def update_posts(
    id: int,
    body: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")

    if not current_user.id == post_query.first().user_id:
        raise HTTPException(status_code=403, detail="it isn't your post")

    post_query.update(body.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()