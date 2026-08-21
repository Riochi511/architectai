from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.architecture.orchestrator import (
    ArchitectureOrchestrator,
)
from app.agents.requirements.engine import (
    RequirementsEngine,
)
from app.agents.orchestrator.context import (
    OrchestrationContext,
)
from app.models.project import Project


def _get_project(
    db: Session,
    context: OrchestrationContext,
) -> Project:
    """
    Resolve the project associated with the orchestration context.
    """

    project = (
        db.query(Project)
        .filter(
            Project.id == context.project_id
        )
        .first()
    )

    if project is None:
        raise ValueError(
            f"Project not found: "
            f"{context.project_id}"
        )

    return project


def make_requirements_adapter(
    db: Session,
):
    """
    Adapt RequirementsEngine to the generic
    orchestrator agent contract.
    """

    engine = RequirementsEngine()

    async def handler(
        context: OrchestrationContext,
    ) -> dict:
        project = _get_project(
            db=db,
            context=context,
        )

        return engine.process(
            project=project,
            db=db,
        )

    return handler


def make_architecture_adapter(
    db: Session,
):
    """
    Adapt ArchitectureOrchestrator to the generic
    orchestrator agent contract.
    """

    engine = ArchitectureOrchestrator()

    async def handler(
        context: OrchestrationContext,
    ) -> dict:
        project = _get_project(
            db=db,
            context=context,
        )

        return engine.generate(
            project=project,
            db=db,
        )

    return handler