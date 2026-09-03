from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password


def get_user_by_email(db: Session, tenant_id: str, email: str) -> User | None:
    return db.query(User).filter(User.tenant_id == tenant_id, User.email == email).first()


def create_user(db: Session, tenant_id: str, data: UserCreate) -> User:
    user = User(
        tenant_id=tenant_id,
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, tenant_id: str) -> list[User]:
    return db.query(User).filter(User.tenant_id == tenant_id).all()


def authenticate_user(db: Session, tenant_id: str, email: str, password: str) -> User | None:
    user = get_user_by_email(db, tenant_id, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
