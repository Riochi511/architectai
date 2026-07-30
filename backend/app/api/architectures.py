from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.user import User
from app.models.project import Project
from app.models.architecture import Architecture

from app.schemas.architecture import ArchitectureResponse

from app.services.architecture_generator import (
    generate_architecture,
)
from app.services.pdf_generator import generate_pdf

router = APIRouter(
    prefix="/architectures",
    tags=["Architectures"],
)


# ----------------------------------------------------
# Generate Architecture
# ----------------------------------------------------
@router.post(
    "/generate/{project_id}",
    response_model=ArchitectureResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_project_architecture(
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
            status_code=404,
            detail="Project not found.",
        )

    architecture_text = generate_architecture(project)

    architecture = Architecture(
        title=f"{project.name} Architecture",
        architecture_type="System Architecture",
        content=architecture_text,
        project_id=project.id,
    )

    db.add(architecture)
    db.commit()
    db.refresh(architecture)

    return architecture


# ----------------------------------------------------
# List All Architectures
# ----------------------------------------------------
@router.get(
    "/",
    response_model=list[ArchitectureResponse],
)
def list_architectures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    architectures = (
        db.query(Architecture)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
        .order_by(Architecture.id.desc())
        .all()
    )

    return architectures


# ----------------------------------------------------
# Get One Architecture
# ----------------------------------------------------
@router.get(
    "/{architecture_id}",
    response_model=ArchitectureResponse,
)
def get_architecture(
    architecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    architecture = (
        db.query(Architecture)
        .join(Project)
        .filter(
            Architecture.id == architecture_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found.",
        )

    return architecture


# ----------------------------------------------------
# Download Architecture PDF
# ----------------------------------------------------
@router.get(
    "/{architecture_id}/pdf",
)
def download_architecture_pdf(
    architecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    architecture = (
        db.query(Architecture)
        .join(Project)
        .filter(
            Architecture.id == architecture_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found.",
        )

    pdf_path = generate_pdf(
        title=architecture.title,
        markdown_content=architecture.content,
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{architecture.title}.pdf",
    )


# ----------------------------------------------------
# Delete Architecture
# ----------------------------------------------------
@router.delete(
    "/{architecture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_architecture(
    architecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    architecture = (
        db.query(Architecture)
        .join(Project)
        .filter(
            Architecture.id == architecture_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not architecture:
        raise HTTPException(
            status_code=404,
            detail="Architecture not found.",
        )

    db.delete(architecture)
    db.commit()

    return None