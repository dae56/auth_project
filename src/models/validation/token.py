from pydantic import BaseModel, Field


class TokenData(BaseModel):
    exp: int
    sub: str
    role: str
