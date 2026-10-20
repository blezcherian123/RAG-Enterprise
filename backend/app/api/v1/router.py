from fastapi import APIRouter

from app.api.v1 import auth, tenants, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
router.include_router(users.router, prefix="/users", tags=["users"])


@router.get("/models", response_model=list[str], tags=["models"])
def get_models():
    """Return all assistant profiles while role-based chat access is deferred."""
    return ["hr", "employee", "finance", "c_level"]
