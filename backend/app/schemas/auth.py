from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=1, max_length=128)
    tenant_id: str | None = Field(default=None, max_length=36)
    tenant_name: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @model_validator(mode="after")
    @classmethod
    def only_one_tenant_selector(cls, model):
        if model.tenant_id and model.tenant_name:
            raise ValueError("Provide only one tenant selector")
        return model


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str | None = None
    tenant_name: str | None = Field(default=None, min_length=3, max_length=128)
