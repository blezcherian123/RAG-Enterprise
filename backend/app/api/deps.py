from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.tenant import Tenant
from app.db.session import get_db
from app.services.tenant_service import get_tenant_by_id


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_tenant_header(request: Request) -> str:
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing tenant header: {settings.TENANT_HEADER}",
        )
    return tenant_id


def get_current_tenant(
    db: Session = Depends(get_db_session),
    tenant_id: str = Depends(get_tenant_header),
) -> Tenant:
    tenant = get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return tenant
