from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.core.security import InvalidTokenError, decode_access_token, oauth2_scheme
from app.db.session import get_db
from app.models.user import User


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_error = BusinessException(
        code=40100,
        message="invalid or expired token",
        status_code=401,
    )

    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_error

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_error

    user = db.get(User, int(user_id))
    if not user:
        raise credentials_error

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise BusinessException(
            code=40300,
            message="inactive user",
            status_code=403,
        )
    return current_user


__all__ = ["get_db", "get_current_user", "get_current_active_user"]