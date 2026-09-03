from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate


def get_tenant_by_id(db: Session, tenant_id: str) -> Tenant | None:
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def get_tenant_by_name(db: Session, name: str) -> Tenant | None:
    return db.query(Tenant).filter(Tenant.name == name).first()


def create_tenant(db: Session, data: TenantCreate) -> Tenant:
    tenant = Tenant(name=data.name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
