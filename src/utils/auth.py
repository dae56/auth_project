import hashlib
import os
import jwt

from src.models.validation.token import TokenData


def get_hash_data(data: str, salt: str) -> str:
    return hashlib.scrypt(password=data.encode(), salt=salt.encode(), n=8, r=512, p=2, dklen=128).hex()


def encode_token(token_data: TokenData) -> str:
    return jwt.encode(
        payload=token_data.model_dump(),
        key=os.getenv('JWT_SALT'),
        algorithm='HS256'
    )


def decode_token(token: str) -> TokenData:
    return TokenData(
        **jwt.decode(
            jwt=token,
            key=os.getenv('JWT_SALT'),
            algorithms=['HS256']
        )
    )
