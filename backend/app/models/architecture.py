from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime, UTC

from app.database.base import Base


class Architecture(Base):
    __tablename__ = "architectures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    architecture_type: Mapped[str] = mapped_column(
        String(100),
        default="System Architecture",
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id")
    )

    project = relationship(
        "Project",
        back_populates="architectures",
    )