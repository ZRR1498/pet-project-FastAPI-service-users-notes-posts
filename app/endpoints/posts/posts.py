import datetime

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.endpoints.posts.models import Posts, Likes
from app.endpoints.posts.schemas import PostCreate, PostUserGet
from app.endpoints.users.auth import AuthToken
from app.utils import check_auth_token


router = APIRouter()


@router.get("/user/posts/", response_model=List[PostUserGet], name="get user's posts", tags=["posts"])
async def get_user_posts(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        posts = db.query(Posts).filter(Posts.user_id == token.user_id).order_by(Posts.created_at.desc()).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Don't found posts")

        return posts


@router.post("/user/posts/", name="create new post", tags=["posts"])
async def create_user_post(token: AuthToken = Depends(check_auth_token), post: PostCreate = Body(..., embed=True),
                           db: Session = Depends(get_db)):
    if token:
        if post.text != "":
            new_post = Posts(
                user_id=token.user_id,
                text=post.text,
                created_at=datetime.datetime.utcnow()
            )

            db.add(new_post)
            db.commit()

            return {f"Create new post with post_id: {new_post.id} is successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill all fields")


@router.get("/user/posts/{post_id}/", response_model=PostUserGet, name="get post", tags=["posts"])
async def get_user_post(token: AuthToken = Depends(check_auth_token), post_id=int, db: Session = Depends(get_db)):
    if token:
        post = db.query(Posts).filter(Posts.user_id == token.user_id, Posts.id == post_id).one_or_none()
        if not post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found post")

        return post


@router.patch("/user/posts/{post_id}/", name="update post", tags=["posts"])
async def update_user_post(token: AuthToken = Depends(check_auth_token), post_id=int,
                           text: PostCreate = Body(..., embed=True),
                           db: Session = Depends(get_db)):
    if token:
        if text.text != "":
            db.query(Posts).filter(Posts.user_id == token.user_id, Posts.id == post_id).\
                update(values={"text": text.text, "updated_at": datetime.datetime.utcnow()})
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill text field")

        return {"Post upgraded successfully"}


@router.delete("/user/posts/{post_id}/", name="delete post", tags=["posts"])
async def delete_user_post(token: AuthToken = Depends(check_auth_token), post_id=int, db: Session = Depends(get_db)):
    if token:
        db.query(Posts).filter(Posts.user_id == token.user_id, Posts.id == post_id).delete()
        check_likes = db.query(Likes).filter(Likes.post_id == Posts.id).one_or_none()
        if check_likes:
            db.query(Likes).filter(Likes.post_id == Posts.id).delete()

        db.commit()

        return {"Post deleted successfully"}


@router.post("/user/posts/{post_id}/", name="post/delete like", tags=["posts"])
async def post_like(token: AuthToken = Depends(check_auth_token), post_id=int, db: Session = Depends(get_db)):
    if token:
        check_like_user = db.query(Likes).filter(Likes.post_id == post_id, Likes.user_id == token.user_id).one_or_none()
        if check_like_user:
            db.query(Likes).filter(Likes.post_id == post_id, Likes.user_id == token.user_id).delete()
            db.query(Posts).filter(Posts.id == post_id).update(values={"likes": Posts.likes - 1})
            db.commit()

            return {"Like was successfully deleted"}

        db.query(Posts).filter(Posts.id == post_id).update(values={"likes": Posts.likes + 1})
        new_like = Likes(
            post_id=int(post_id),
            user_id=token.user_id
        )
        db.add(new_like)
        db.commit()

        return {"Like was successfully placed"}


@router.get("/users/{user_id}/posts/", response_model=List[PostUserGet], name="get user's posts", tags=["posts"])
async def get_users_posts(token: AuthToken = Depends(check_auth_token), user_id=int, db: Session = Depends(get_db)):
    if token:
        posts = db.query(Posts).filter(Posts.user_id == user_id).order_by(Posts.created_at.desc()).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Not found posts this user")

        return posts


@router.get("/users/{user_id}/posts/{post_id}/", response_model=PostUserGet, name="get user's post", tags=["posts"])
async def get_users_post(token: AuthToken = Depends(check_auth_token), user_id=int, post_id=int,
                         db: Session = Depends(get_db)):
    if token:
        post = db.query(Posts).filter(Posts.user_id == user_id, Posts.id == post_id).one_or_none()
        if not post:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Not found post")

        return post
