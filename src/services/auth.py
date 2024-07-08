from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import setting
from .crud_user import RepoUsers
from ..database import get_db
from sqlalchemy.orm import Session


def create_access_token(subject: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "expire": (expire + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "sub": subject,
        "iat": datetime.utcnow(),
        "iss": "api_restfull:todo"}
    encoded_jwt_token = jwt.encode(to_encode, setting.secret_key, setting.algorithm)
    return encoded_jwt_token


def decode_token(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, setting.secret_key, setting.algorithm)
        return payload
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return None


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Get current user id from JWT token
    """
    token = credentials.credentials
    print(token)

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    return user_id


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        db: Session = Depends(get_db)
):
    """
    Get current user obj from JWT token
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token",
    )
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise credentials_exc
    current_user_id = payload.get("sub")
    if not current_user_id:
        raise credentials_exc
    current_user = RepoUsers.get_user_by_id(db=db, id=current_user_id)
    return current_user



# def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)
#
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, setting.refresh_secret_key, setting.algorithm)
#     return encoded_jwt
