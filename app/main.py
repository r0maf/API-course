from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="PostRomagres8876",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Database connection was failed")
    print(f"Error: {error}")
    time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchone()
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="we cannot find your post")


@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY id""")
    posts = cursor.fetchall()
    return posts


@app.post("/posts")
def create_post(post: Post):
    query = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    values = (post.title, post.content, post.published)
    cursor.execute(query, values)
    conn.commit()
    return {"message": "The post was successfully created"}


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING True""")
    posts = cursor.fetchone()
    if posts:
        conn.commit()
        yield Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="sorry, your element doesn't exist")


@app.put("/posts/{id}")
def update_post(id: int, body: Post):
    query = f"""UPDATE posts SET title = %s, content = %s, published = %s, created_at = now() 
                WHERE id = {id} RETURNING *"""
    values = (body.title, body.content, body.published)
    cursor.execute(query, values)
    post = cursor.fetchone()
    if post:
        conn.commit()
        return {
            "information": {
                "message": "The post was successfully updated",
                "updated_post": post,
            }
        }
    else:
        raise HTTPException(status_code=404, detail="sorry, the id doesn't exist")
