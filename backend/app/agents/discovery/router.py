from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.project import Project

from app.agents.discovery.engine import DiscoveryEngine
from app.agents.discovery.schemas import DiscoveryRequest

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"],
)

engine = DiscoveryEngine()


@router.post("/start/{project_id}")
def start_discovery(
    project_id: int,
    request: DiscoveryRequest,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    result = engine.process(
        project=project,
        user_message=request.user_message,
    )

    db.commit()
    db.refresh(project)

    return {
        "next_question": result["question"],
        "stage": project.discovery_stage,
        "confidence_score": project.discovery_confidence,
        "completed": result["completed"],
    }