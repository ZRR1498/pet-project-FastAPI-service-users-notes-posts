from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
import uuid

from app.db.database import get_db
from app.utils import get_password_hash
from app.endpoints.users.models import Users, AuthToken
from app.endpoints.users.schemas import UserLoginForm, UserCreateForm
from app.utils import check_auth_token


router = APIRouter()


@router.post("/login", name="users:login", tags=["authorization"])
async def login(user_form: UserLoginForm = Body(..., embed=True), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.hash_password:
        return {"error": "Email/password invalid"}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    db.add(auth_token)
    db.commit()
    return {"auth_token": auth_token.token}


@router.post("/sign_up", name="users:sign_up", tags=["authorization"])
async def create_user(user: UserCreateForm = Body(..., embed=True), db: Session = Depends(get_db)):
    check_email = db.query(Users.id).filter(Users.email == user.email).one_or_none()
    check_nickname = db.query(Users.id).filter(Users.nickname == user.nickname).one_or_none()

    if check_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    if check_nickname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nickname already exists")

    new_user = Users(
        email=user.email,
        hash_password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        nickname=user.nickname,
        is_active=user.is_active,
    )
    db.add(new_user)
    db.commit()
    return {"user_id": new_user.id}


@router.delete("/logout", name="users:logout", tags=["authorization"])
async def logout(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        db.query(AuthToken).filter(AuthToken.token == token.token).delete()
        db.commit()
        return {"User logout"}
