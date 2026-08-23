from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.architecture.orchestrator import (
    ArchitectureOrchestrator,
)
from app.agents.discovery.schemas import (
    DiscoveryStage,
)
from app.agents.requirements.engine import (
    RequirementsEngine,
)
from app.agents.technology.engine import (
    TechnologyEngine,
)
from app.agents.technology.prompts import (
    SYSTEM_PROMPT as TECHNOLOGY_SYSTEM_PROMPT,
    TECHNOLOGY_DECISIONS_PROMPT,
)
from app.agents.technology.validator import (
    validate as validate_technology,
)
from app.agents.technology.confidence import (
    calculate_confidence as calculate_technology_confidence,
)
from app.agents.database.engine import (
    DatabaseEngine,
)
from app.agents.database.prompts import (
    SYSTEM_PROMPT as DATABASE_SYSTEM_PROMPT,
    DATABASE_DESIGN_PROMPT,
)
from app.agents.database.validator import (
    validate as validate_database,
)
from app.agents.database.confidence import (
    calculate_confidence as calculate_database_confidence,
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


def make_discovery_adapter(
    db: Session,
):
    """
    Adapt the completed Discovery state to the
    generic orchestrator agent contract.

    Discovery itself remains interactive and is handled
    by DiscoveryEngine through the Discovery API.

    This adapter only allows the orchestrator to consume
    the completed discovery result.
    """

    async def handler(
        context: OrchestrationContext,
    ) -> dict:
        project = _get_project(
            db=db,
            context=context,
        )

        if (
            project.discovery_stage
            != DiscoveryStage.COMPLETE.value
        ):
            raise ValueError(
                "Project discovery is not complete."
            )

        return project.discovery_memory or {}

    return handler


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


def make_technology_adapter(
    db: Session,
):
    """
    Adapt TechnologyEngine to the generic
    orchestrator agent contract.

    Technology consumes:

    - completed discovery memory
    - validated requirements
    - generated architecture

    The adapter does not modify orchestration state directly.
    It returns a structured result for the Orchestrator to store.
    """

    engine = TechnologyEngine()

    async def handler(
        context: OrchestrationContext,
    ) -> dict:

        project = _get_project(
            db=db,
            context=context,
        )

        if not context.discovery_memory:
            raise ValueError(
                "Discovery memory is required "
                "before technology decisions."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before technology decisions."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before technology decisions."
            )

        architecture_record = context.architecture.get(
            "architecture"
        )

        if architecture_record is None:
            raise ValueError(
                "Architecture output does not contain "
                "the generated architecture."
            )

        architecture_document = getattr(
            architecture_record,
            "content",
            None,
        )

        if not architecture_document:
            raise ValueError(
                "Generated architecture document "
                "is empty."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": (
                context.discovery_memory
            ),
            "requirements": (
                context.requirements
            ),
            "architecture": architecture_document,
            "architecture_validation": (
                context.architecture.get(
                    "validation",
                    {},
                )
            ),
            "architecture_confidence": (
                context.architecture.get(
                    "confidence_score"
                )
            ),
        }

        document = engine.generate(
            system_prompt=TECHNOLOGY_SYSTEM_PROMPT,
            section_prompt=TECHNOLOGY_DECISIONS_PROMPT,
            project_context=project_context,
        )

        validation = validate_technology(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_technology_confidence(
                validation
            )
        )

        return {
            "technology_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler


def make_database_adapter(
    db: Session,
):
    """
    Adapt DatabaseEngine to the generic
    orchestrator agent contract.

    Database design consumes:

    - completed discovery memory
    - validated requirements
    - generated architecture
    - approved technology decisions

    The adapter generates the database design, validates it,
    calculates database readiness, and returns the structured
    result to the Orchestrator.
    """

    engine = DatabaseEngine()

    async def handler(
        context: OrchestrationContext,
    ) -> dict:

        project = _get_project(
            db=db,
            context=context,
        )

        if not context.discovery_memory:
            raise ValueError(
                "Discovery memory is required "
                "before database design."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before database design."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before database design."
            )

        if not context.technology:
            raise ValueError(
                "Technology decisions are required "
                "before database design."
            )

        architecture_record = context.architecture.get(
            "architecture"
        )

        if architecture_record is None:
            raise ValueError(
                "Architecture output does not contain "
                "the generated architecture."
            )

        architecture_document = getattr(
            architecture_record,
            "content",
            None,
        )

        if not architecture_document:
            raise ValueError(
                "Generated architecture document "
                "is empty."
            )

        technology_document = context.technology.get(
            "technology_document"
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the generated technology document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": (
                context.discovery_memory
            ),
            "requirements": (
                context.requirements
            ),
            "architecture": architecture_document,
            "architecture_validation": (
                context.architecture.get(
                    "validation",
                    {},
                )
            ),
            "architecture_confidence": (
                context.architecture.get(
                    "confidence_score"
                )
            ),
            "technology": technology_document,
            "technology_validation": (
                context.technology.get(
                    "validation",
                    {},
                )
            ),
            "technology_confidence": (
                context.technology.get(
                    "confidence_score"
                )
            ),
        }

        document = engine.generate(
            system_prompt=DATABASE_SYSTEM_PROMPT,
            section_prompt=DATABASE_DESIGN_PROMPT,
            project_context=project_context,
        )

        validation = validate_database(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_database_confidence(
                validation
            )
        )

        return {
            "database_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler