import hashlib

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.configs import SECRET_KEY
from app.endpoints.users.models import AuthToken
from app.db.database import get_db


def check_auth_token(token: str, db: Session = Depends(get_db)):
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).one_or_none()
    if auth_token:
        return auth_token

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


def get_password_hash(password: str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf8')).hexdigest()
