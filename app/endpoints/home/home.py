from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.utils import check_auth_token
from app.db.database import get_db
from app.endpoints.users.models import AuthToken
from app.endpoints.posts.models import Posts
from app.endpoints.users.models import UserFriends


router = APIRouter()


@router.get("/", name=" get all posts friend's", tags=["home"])
async def home(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if not token:
        return {"Some thing displayed to unauthorized users"}
    else:
        posts = db.query(Posts).filter(Posts.user_id == UserFriends.second_user_id).\
            filter(UserFriends.first_user_id == token.user_id, UserFriends.status_accepted == True).\
            order_by(Posts.created_at.desc()).all()

        if not posts:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found news/posts")

        return posts


@router.get("/recommendations", name="get all posts subscriptions", tags=["home"])
async def home(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if not token:
        return {"Some thing displayed to unauthorized users"}
    else:
        posts = db.query(Posts).filter(Posts.user_id == UserFriends.second_user_id).\
            filter(UserFriends.first_user_id == token.user_id, UserFriends.status_accepted == False).\
            order_by(Posts.created_at.desc()).all()

        if not posts:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found news/posts")

        return posts
