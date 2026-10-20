from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.revoked_token import RevokedToken
from app.models.user import User
from app.schemas.user import UserRole
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db_session)],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
        tenant_id = payload["tenant_id"]
        token_id = payload.get("jti")
    except (ValueError, KeyError, TypeError):
        raise unauthorized from None

    if token_id and db.query(RevokedToken.jti).filter(RevokedToken.jti == token_id).first():
        raise unauthorized
    user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_roles(*roles: UserRole):
    allowed = set(roles)

    def check_role(user: Annotated[User, Depends(get_current_user)]) -> User:
        if UserRole(user.role) not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return check_role
