from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, tenant_id: str, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.tenant_id == tenant_id)
        .filter(User.email == email)
        .first()
    )


def create_user(db: Session, tenant_id: str, user_in: UserCreate) -> User:
    user = User(
        tenant_id=tenant_id,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, tenant_id: str) -> list[User]:
    return db.query(User).filter(User.tenant_id == tenant_id).all()


def authenticate_user(db: Session, tenant_id: str, email: str, password: str) -> User | None:
    user = get_user_by_email(db, tenant_id, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
