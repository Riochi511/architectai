from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.project import Project
from app.models.requirement import Requirement
from app.models.user import User
from app.schemas.requirement import (
    RequirementCreate,
    RequirementUpdate,
    RequirementResponse,
)

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"],
)


@router.post(
    "/project/{project_id}",
    response_model=RequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_requirement(
    project_id: int,
    requirement: RequirementCreate,
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

    new_requirement = Requirement(
        title=requirement.title,
        description=requirement.description,
        category=requirement.category,
        priority=requirement.priority,
        project_id=project.id,
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement


@router.get(
    "/project/{project_id}",
    response_model=list[RequirementResponse],
)
def get_project_requirements(
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

    return (
        db.query(Requirement)
        .filter(Requirement.project_id == project.id)
        .all()
    )


@router.get(
    "/{requirement_id}",
    response_model=RequirementResponse,
)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requirement = (
        db.query(Requirement)
        .join(Project)
        .filter(
            Requirement.id == requirement_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found.",
        )

    return requirement


@router.put(
    "/{requirement_id}",
    response_model=RequirementResponse,
)
def update_requirement(
    requirement_id: int,
    updated: RequirementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requirement = (
        db.query(Requirement)
        .join(Project)
        .filter(
            Requirement.id == requirement_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found.",
        )

    requirement.title = updated.title
    requirement.description = updated.description
    requirement.category = updated.category
    requirement.priority = updated.priority

    db.commit()
    db.refresh(requirement)

    return requirement


@router.delete(
    "/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requirement = (
        db.query(Requirement)
        .join(Project)
        .filter(
            Requirement.id == requirement_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found.",
        )

    db.delete(requirement)
    db.commit()

    return None