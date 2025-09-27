from enum import Enum

from pydantic import BaseModel, Field, EmailStr

class RoleEnumCreate(str, Enum):
    admin = "admin"
    user = "user"


class UserCreate(BaseModel):
    first_name: str = Field(min_length=8, max_length=100)
    last_name: str = Field(min_length=8, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
