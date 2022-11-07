import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse
from typing import List, Union

from app.db.database import get_db
from app.endpoints.users.models import Users, AuthToken, UserFriends
from app.endpoints.users.schemas import UsersAll, UserGetByNickname, UserId
from app.utils import check_auth_token
from app.endpoints.users.services import get_users_by


router = APIRouter()


@router.get("/users/", response_model=List[UsersAll], name="all_users:get", tags=["users"])
async def get_all_users(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        users = db.query(Users).filter(Users.is_active).all()

        return users


@router.post("/users/", name="following", tags=["users"])
async def following_to_user(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db),
                            user_id: UserId = Body(..., embed=True)):
    if token:
        check_exist_foll = db.query(UserFriends).filter(UserFriends.first_user_id == token.user_id,
                                                        UserFriends.second_user_id == user_id.id).one_or_none()
        if check_exist_foll:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You have already subscribed to this user")

        if user_id.id != token.user_id and user_id.id != 0:
            new_following = UserFriends(
                first_user_id=token.user_id,
                second_user_id=user_id.id,
                status_accepted=False,
                date_time=datetime.datetime.utcnow()
            )

            db.add(new_following)
            db.commit()

            return {f"You have successfully subscribed to the user: {user_id.id}"}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add yourself as a friend")


@router.get("/users/search/", response_model=List[UserGetByNickname], name="users_by_attrs:get", tags=["users"])
async def get_users_by_attrs(token: AuthToken = Depends(check_auth_token),
                             nickname: Union[str] = Query(default=None),
                             first_name: Union[str] = Query(default=None),
                             last_name: Union[str] = Query(default=None),
                             db: Session = Depends(get_db)):
    if token:
        users = get_users_by(nickname, first_name, last_name, db, Users, HTTPException, status)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found")

        return users


@router.get("/users/{nickname}/", response_model=UserGetByNickname, name="selected_user:get", tags=["users"])
async def get_selected_user(token: AuthToken = Depends(check_auth_token), nickname=str, db: Session = Depends(get_db)):
    if token:
        user = db.query(Users).filter(Users.nickname == nickname).one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        return user


@router.get("/users/{nickname}/avatar/", response_model=UserGetByNickname, name="selected_user:get", tags=["users"])
async def get_user_avatar(token: AuthToken = Depends(check_auth_token), nickname=str, db: Session = Depends(get_db)):
    if token:
        user = db.query(Users.nickname, Users.avatar).filter(Users.nickname == nickname).one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        if not user.avatar:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The users does not have an avatar")

        return FileResponse(user.avatar)
