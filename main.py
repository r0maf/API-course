from typing import Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

posts = {"posts_IDs": {}}


class Post(BaseModel):
    addition_inf: Optional[str] = None
    id: int
    title: str
    content: Any
    rating: Optional[int] = None


@app.get("/posts/{id}")
def get_posts(id):
    if int(id) in posts["posts_IDs"]:
        return posts["posts_IDs"][int(id)]
    else:
        HTTPException(status_code=404, detail="we cannot find your post")


@app.get("/posts")
def get_all_posts():
    return posts["posts_IDs"]


@app.post("/posts")
def create_posts(post: Post):
    if post.id not in posts["posts_IDs"]:
        posts["posts_IDs"][post.id] = post.model_dump()
        return {
            "message": f"post <<{post.title}>> has just been created",
            "post": posts["posts_IDs"][post.id],
        }
    else:
        raise HTTPException(409, detail="sorry, but the id already exists")
