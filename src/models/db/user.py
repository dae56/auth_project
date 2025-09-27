import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped


from src.models.db.base import Base


class RoleUser(enum.Enum):
    admin = 'admin',
    user = 'user'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(253), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    role: Mapped[RoleUser]
