import datetime
import shutil

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from app.utils import check_auth_token
from app.db.database import get_db
from app.endpoints.users.models import Users, AuthToken, UserFriends
from app.endpoints.users.schemas import UserProfile, UserUpdateData, UsersAll, UserId
from app.utils import get_password_hash


router = APIRouter()


@router.get("/user/profile", response_model=UserProfile, name="current_user:get", tags=["user_profile"])
async def get_current_user(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == token.user_id).one_or_none()

    return user


@router.get("/user/profile/avatar", name="current_user_avatar:get", tags=["user_profile"])
async def get_avatar_user(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    user_avatar = db.query(Users.avatar).filter(Users.id == token.user_id).one_or_none()

    if not user_avatar.avatar:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You does not have an avatar")

    return FileResponse(user_avatar[0])


@router.patch("/user/profile/settings", response_model=UserProfile, name="update_user_settings:patch",
              tags=["user_profile"])
async def update_current_user(user: UserUpdateData = Body(..., embed=True),
                              token: AuthToken = Depends(check_auth_token),
                              db: Session = Depends(get_db)):
    check_exist_email = db.query(Users.id).filter(Users.email == user.email).one_or_none()
    if check_exist_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    data = {}
    check_data = user.dict()
    for attr in check_data:
        if check_data[attr] != "":
            if attr == "password":
                data["hash_password"] = get_password_hash(check_data[attr])
                continue
            data[attr] = check_data[attr]

    db.query(Users).where(Users.id == token.user_id).update(values=data)
    db.commit()

    user = db.query(Users).filter(Users.id == token.user_id).one_or_none()

    return user


@router.patch("/user/profile/settings/avatar", name="update_user_avatar:patch", tags=["user_profile"])
async def update_avatar_user(
        image: UploadFile = File(...),
        token: AuthToken = Depends(check_auth_token),
        db: Session = Depends(get_db)
):
    path_avatar = f"app/endpoints/users/avatars/{token.user_id}.png"
    if image:
        with open(path_avatar, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    db.query(Users).where(Users.id == token.user_id).update(values={"avatar": path_avatar})
    db.commit()

    return {"Avatar created successfully!"}


@router.get("/user/followers/", response_model=List[UsersAll], name="get all user's followers", tags=["user_friends"])
async def get_user_followers(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        followers = db.query(Users).filter(Users.id == UserFriends.first_user_id). \
            filter(UserFriends.second_user_id == token.user_id, UserFriends.status_accepted == False).all()

        if not followers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found followers")

        return followers


@router.post("/user/followers/", name="add new friend from user's followers", tags=["user_friends"])
async def update_user_followers(token: AuthToken = Depends(check_auth_token), user_id: UserId = Body(..., embed=True),
                                db: Session = Depends(get_db)):
    if token:
        check_exist_friend = db.query(UserFriends).filter(UserFriends.first_user_id == token.user_id,
                                                          UserFriends.second_user_id == user_id.id).one_or_none()
        if check_exist_friend:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already have this user as a friend")

        db.query(UserFriends).filter(UserFriends.second_user_id == token.user_id,
                                     UserFriends.first_user_id == user_id.id, UserFriends.status_accepted == False). \
            update(values={"status_accepted": True})

        new_friend = UserFriends(
            first_user_id=token.user_id,
            second_user_id=user_id.id,
            status_accepted=True,
            date_time=datetime.datetime.utcnow()
        )
        db.add(new_friend)
        db.commit()

        return new_friend


@router.delete("/user/followers/", name="delete user's follower", tags=["user_friends"])
async def delete_user_followers(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db),
                                user_id: UserId = Body(..., embed=True)):
    if token:
        db.query(UserFriends).filter(UserFriends.second_user_id == token.user_id,
                                     UserFriends.first_user_id == user_id.id,
                                     UserFriends.status_accepted == False).delete()
        db.commit()

        return {f"You have successfully deleted a follower: {user_id.id}"}


@router.get("/user/friends/", response_model=List[UsersAll], name="get all user's friends", tags=["user_friends"])
async def get_user_friends(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        friends = db.query(Users).filter(Users.id == UserFriends.second_user_id). \
            filter(UserFriends.first_user_id == token.user_id, UserFriends.status_accepted == True).all()

        if not friends:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found friends")

        return friends


@router.delete("/user/friends/", name="delete friend", tags=["user_friends"])
async def delete_user_friends(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db),
                              user_id: UserId = Body(..., embed=True)):
    if token:
        db.query(UserFriends).filter(UserFriends.second_user_id == token.user_id,
                                     UserFriends.first_user_id == user_id.id, UserFriends.status_accepted == True). \
            update(values={"status_accepted": False})

        db.query(UserFriends).filter(UserFriends.first_user_id == token.user_id,
                                     UserFriends.second_user_id == user_id.id).delete()
        db.commit()

        return {f"You have successfully deleted a friend: {user_id.id}"}
