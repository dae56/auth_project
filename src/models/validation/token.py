from pydantic import BaseModel, Field


class TokenData(BaseModel):
    exp: int
    sub: str
    role: str


class Token(BaseModel):
    token: str = Field(max_length=256)
