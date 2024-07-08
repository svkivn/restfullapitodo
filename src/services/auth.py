from datetime import datetime, timedelta
import jwt

import setting
from ..models.user import User


def create_access_token(user: User, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": user.username, "iss": "api_restfull"}
    encoded_jwt_token = jwt.encode(to_encode, setting.secret_key, setting.algorithm)
    return encoded_jwt_token


def decode_token(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, setting.secret_key, setting.algorithm)
        return payload
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return None



# def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)
#
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, setting.refresh_secret_key, setting.algorithm)
#     return encoded_jwt
