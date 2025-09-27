import os
import datetime

import jwt

from fastapi import APIRouter, Request, status, HTTPException
from sqlalchemy import text, select
from sqlalchemy.exc import IntegrityError


from src.connectors.db import get_session
from src.models.db.user import User, RoleUser
from src.models.errors.exc import DuplicateEmail
from src.models.validation.token import TokenData
from src.utils.auth import get_hash_data, encode_token, decode_token
from src.models.validation.user import UserCreate, UserLogin


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/health-check")
def health_check() -> dict[str, dict[str, str | int]]:
    return {
        "app": {
            "status_code": status.HTTP_200_OK,
            "detail": "app is running."
        },
        "db": {
            "status_code": status.HTTP_200_OK if get_session().scalar(text("SELECT 1")) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "db is running." if get_session().scalar(text("SELECT 1")) else "db is unavailable."
        }
    }


@router.post("/registry")
def registry(new_user_data: UserCreate, request: Request):
    header_role = request.headers.get("Role")
    if header_role == "admin":
        session = get_session()
        try:
            user = User(
                first_name=new_user_data.first_name,
                last_name=new_user_data.last_name,
                email=new_user_data.email,
                password_hash=get_hash_data(new_user_data.password, os.getenv("PASS_SALT")),
                role=RoleUser.user
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError as e:
            session.rollback()
            if e.code == "gkpj":
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(DuplicateEmail(e.params.get("email")))
                )
        else:
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "User registered successfully.",
                "info": {
                    "user_id": user.id,
                    "email": user.email,
                    "last_name": user.last_name,
                    "first_name": user.first_name,
                    "role": user.role,
                    "is_active": user.is_active
                }
            }
    elif header_role != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions."
        )
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated."
    )


@router.post("/login")
def login(user_data: UserLogin):
    session = get_session()
    res: User | None = session.execute(select(User).where(User.email == user_data.email)).scalar()
    if res:
        if res.password_hash == get_hash_data(user_data.password, os.getenv("PASS_SALT")):
            return encode_token(
                TokenData(
                    exp=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)).timestamp()),
                    sub=str(res.id),
                    role=res.role.value[0]
                )
            )
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found."
    )


@router.post("/get-data-from-token")
def get_data_from_token(request: Request):
    try:
        header_authorization: str | None = request.headers.get("Authorization")
        if header_authorization:
            return decode_token(header_authorization.split(" ")[1])
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
    except jwt.ExpiredSignatureError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired."
        )
    except jwt.InvalidTokenError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token."
        )
