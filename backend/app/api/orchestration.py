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


router = APIRouter(
    prefix="/orchestration",
    tags=["Orchestration"],
)


@router.post(
    "/run/{project_id}",
)
async def run_project_orchestration(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not project:
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

    state = await orchestrator.run(
        context,
    )

    return {
        "project_id": project.id,
        "status": state.status,
        "completed_stages": state.completed_stages,
        "current_stage": state.current_stage,
    }