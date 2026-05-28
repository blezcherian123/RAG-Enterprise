from pydantic import BaseModel, Field


class TenantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)


class TenantCreate(TenantBase):
    pass


class TenantOut(TenantBase):
    id: str

    class Config:
        orm_mode = True
