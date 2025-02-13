from typing import Any, Optional
from fastapi import Body, FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

posts = {}


class Post(BaseModel):
    id: int
    title: str
    content: Any
    addition_inf: Optional[str] = None
    rating: Optional[int] = None


@app.get("/posts/{id}")
def get_post(id: int):
    if id in posts:
        return posts[id]
    else:
        raise HTTPException(status_code=404, detail="we cannot find your post")


@app.get("/posts")
def get_all_posts():
    return posts


@app.post("/posts")
def create_posts(post: Post):
    if post.id not in posts:
        posts[post.id] = post.model_dump(exclude="id")
        return {
            "message": f"post <<{post.title}>> has just been created",
            "post_id": post.id,
            "post": posts[post.id],
        }
    else:
        raise HTTPException(409, detail="sorry, but the id already exists")


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    if id in posts:
        del posts[id]
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")


@app.put("/posts/{id}")
def update_post(id: int, body: dict = Body(...)):
    if id in posts:
        for i in body:
            posts[id][i] = body[i]
        return {"updated_post": posts[id]}
    else:
        raise HTTPException(status_code=404, detail="sorry, the id doesn't exist")
