from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    JSON,
    Float,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150)
    )

    description: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # -----------------------------
    # Discovery Agent Memory
    # -----------------------------

    discovery_stage: Mapped[str] = mapped_column(
        String(50),
        default="vision"
    )

    discovery_memory: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )

    discovery_confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    # -----------------------------
    # Requirements Agent Document
    # -----------------------------

    requirements_document: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )

    # -----------------------------
    # Relationships
    # -----------------------------

    owner = relationship(
        "User",
        back_populates="projects",
    )

    requirements = relationship(
        "Requirement",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    architectures = relationship(
        "Architecture",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    orchestration_runs = relationship(
        "OrchestrationRun",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="OrchestrationRun.created_at",
    )
