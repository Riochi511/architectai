from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    category: Mapped[str] = mapped_column(
        String(50)
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="Medium",
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id")
    )

    project = relationship(
        "Project",
        back_populates="requirements",
    )