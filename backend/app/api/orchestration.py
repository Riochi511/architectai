from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.project import Project
from app.models.user import User
from app.models.orchestration_run import OrchestrationRun

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


def _serialize_state_results(
    state,
) -> dict:
    return jsonable_encoder(
        state.results
    )


def _get_owned_project(
    project_id: int,
    db: Session,
    current_user: User,
) -> Project:
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

    return project


def _get_latest_orchestration_run(
    project_id: int,
    db: Session,
) -> OrchestrationRun:
    orchestration_run = (
        db.query(OrchestrationRun)
        .filter(
            OrchestrationRun.project_id
            == project_id
        )
        .order_by(
            OrchestrationRun.id.desc()
        )
        .first()
    )

    if orchestration_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orchestration run found.",
        )

    return orchestration_run


@router.post(
    "/run/{project_id}",
)
async def run_project_orchestration(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_owned_project(
        project_id=project_id,
        db=db,
        current_user=current_user,
    )

    context = OrchestrationContext(
        project_id=project.id,
    )

    orchestration_run = OrchestrationRun(
        project_id=project.id,
        status="running",
        current_stage=None,
        completed_stages=[],
        results={},
        metadata_json={},
    )

    db.add(orchestration_run)
    db.commit()
    db.refresh(orchestration_run)

    orchestrator = build_orchestrator(
        db=db,
    )

    try:
        state = await orchestrator.run(
            context,
        )

        orchestration_run.status = (
            state.status.value
            if hasattr(
                state.status,
                "value",
            )
            else str(
                state.status
            )
        )

        orchestration_run.current_stage = (
            state.current_stage
        )

        orchestration_run.completed_stages = (
            list(
                state.completed_stages
            )
        )

        orchestration_run.results = (
            _serialize_state_results(
                state
            )
        )

        orchestration_run.metadata_json = (
            jsonable_encoder(
                state.metadata
            )
        )

        orchestration_run.error = None

        db.commit()
        db.refresh(
            orchestration_run
        )

    except Exception as exc:

        orchestration_run.status = "failed"
        orchestration_run.error = str(exc)

        db.commit()
        db.refresh(
            orchestration_run
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail="Project orchestration failed.",
        ) from exc

    return {
        "project_id": project.id,
        "run_id": orchestration_run.id,
        "status": state.status,
        "completed_stages": state.completed_stages,
        "current_stage": state.current_stage,
        "outputs": {
            "requirements": context.requirements,
            "architecture": context.architecture,
            "technology": context.technology,
            "database": context.database,
            "cost": context.cost,
            "critic": context.critic,
            "blueprint": context.blueprint,
            "workforce": context.workforce,
        },
    }


@router.get(
    "/{project_id}/status",
)
def get_project_orchestration_status(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_owned_project(
        project_id=project_id,
        db=db,
        current_user=current_user,
    )

    orchestration_run = (
        _get_latest_orchestration_run(
            project_id=project.id,
            db=db,
        )
    )

    return {
        "project_id": project.id,
        "run_id": orchestration_run.id,
        "status": orchestration_run.status,
        "current_stage": (
            orchestration_run.current_stage
        ),
        "completed_stages": (
            orchestration_run.completed_stages
        ),
        "error": orchestration_run.error,
        "created_at": (
            orchestration_run.created_at
        ),
        "updated_at": (
            orchestration_run.updated_at
        ),
    }


@router.get(
    "/{project_id}/outputs",
)
def get_project_orchestration_outputs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_owned_project(
        project_id=project_id,
        db=db,
        current_user=current_user,
    )

    orchestration_run = (
        _get_latest_orchestration_run(
            project_id=project.id,
            db=db,
        )
    )

    return {
        "project_id": project.id,
        "run_id": orchestration_run.id,
        "status": orchestration_run.status,
        "completed_stages": (
            orchestration_run.completed_stages
        ),
        "outputs": (
            orchestration_run.results
        ),
    }