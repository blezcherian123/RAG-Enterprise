from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so that they are registered with SQLAlchemy metadata.
from app.models import tenant, user  # noqa: F401, E402
