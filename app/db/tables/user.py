import datetime
import uuid

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
