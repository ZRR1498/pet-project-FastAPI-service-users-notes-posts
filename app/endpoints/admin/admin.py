from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from app.endpoints.users.models import Users
from app.db.database import get_db
from app.endpoints.admin.auth_handler import signJWT
from app.endpoints.admin.auth_bearer import JWTBearer
from app.endpoints.admin.schemas import UserLoginSchema, UsersGet, UserId


router = APIRouter()


users = [{"email": "admin@gmail.com", "password": "123456"}]


def check_user(data: UserLoginSchema):
    for admin in users:
        if admin["email"] == data.email and admin["password"] == data.password:
            return True
    return False


@router.post("/admin/login", name="admin:login", tags=["admin"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)

    return {
        "error": "Wrong login details!"
    }


@router.get("/admin/users", response_model=List[UsersGet], dependencies=[Depends(JWTBearer())], name="get_all_users",
            tags=["admin"])
async def get_users(db: Session = Depends(get_db)):
    all_users = db.query(Users).all()

    if not all_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found users")

    return all_users


@router.delete("/admin/users", response_model=List[UsersGet], dependencies=[Depends(JWTBearer())], name="delete_user",
               tags=["admin"])
async def delete_user(db: Session = Depends(get_db), user_id: UserId = Body(..., embed=True)):
    db.query(Users).where(Users.id == user_id.id).delete()
    db.commit()

    all_users = db.query(Users).all()

    if not all_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found users")

    return all_users
