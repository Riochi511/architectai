from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.project import Project
from app.models.user import User

from app.agents.orchestrator.bootstrap import (
    build_orchestrator,
)
from app.agents.orchestrator.context import (
    OrchestrationContext,
)

from app.schemas.orchestration import (
    OrchestrationResponse,
)


router = APIRouter(
    prefix="/orchestration",
    tags=["Orchestration"],
)


@router.post(
    "/run/{project_id}",
    response_model=OrchestrationResponse,
    status_code=status.HTTP_200_OK,
)
async def run_project_orchestration(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrchestrationResponse:

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    context = OrchestrationContext(
        project_id=project.id,
    )

    orchestrator = build_orchestrator(
        db=db,
    )

    try:
        state = await orchestrator.run(
            context,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Project orchestration failed.",
        ) from exc

    return OrchestrationResponse(
        project_id=project.id,
        status=state.status,
        completed_stages=state.completed_stages,
        current_stage=state.current_stage,
        outputs={
            "requirements": context.requirements,
            "architecture": context.architecture,
            "technology": context.technology,
            "database": context.database,
            "cost": context.cost,
            "critic": context.critic,
            "blueprint": context.blueprint,
            "workforce": context.workforce,
        },
    )