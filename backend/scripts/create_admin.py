"""Create the first workspace administrator from a trusted deployment shell."""
import getpass
import sys

from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.tenant import Tenant
from app.schemas.user import UserCreate, UserRole
from app.services.user import create_user, get_user_by_email


def main() -> int:
    email = input("Administrator email: ").strip().lower()
    password = getpass.getpass("Administrator password (min 12 characters): ")
    if len(password) < 12:
        print("Password must be at least 12 characters.", file=sys.stderr)
        return 2

    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.name == "default").one_or_none()
        if tenant is None:
            print("Default workspace is missing. Apply Alembic migrations first.", file=sys.stderr)
            return 2
        if get_user_by_email(db, tenant.id, email):
            print("An account already exists for that email in the default workspace.", file=sys.stderr)
            return 2
        data = UserCreate(email=email, password=password, role=UserRole.ADMIN)
        create_user(db, tenant.id, data)
        print("Workspace administrator created.")
        return 0
    except (ValueError, IntegrityError) as exc:
        db.rollback()
        print(f"Could not create administrator: {exc}", file=sys.stderr)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
