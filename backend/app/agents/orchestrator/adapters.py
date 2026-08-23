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
from app.agents.cost.engine import (
    CostEngine,
)
from app.agents.cost.prompts import (
    SYSTEM_PROMPT as COST_SYSTEM_PROMPT,
    COST_ESTIMATION_PROMPT,
)
from app.agents.cost.validator import (
    validate as validate_cost,
)
from app.agents.cost.confidence import (
    calculate_confidence as calculate_cost_confidence,
)
from app.agents.critic.engine import (
    CriticEngine,
)
from app.agents.critic.prompts import (
    SYSTEM_PROMPT as CRITIC_SYSTEM_PROMPT,
    CRITIC_PROMPT,
)
from app.agents.critic.validator import (
    validate as validate_critic,
)
from app.agents.critic.confidence import (
    calculate_confidence as calculate_critic_confidence,
)
from app.agents.blueprint.engine import (
    BlueprintEngine,
)
from app.agents.blueprint.prompts import (
    SYSTEM_PROMPT as BLUEPRINT_SYSTEM_PROMPT,
    BLUEPRINT_PROMPT,
)
from app.agents.blueprint.validator import (
    validate as validate_blueprint,
)
from app.agents.blueprint.confidence import (
    calculate_confidence as calculate_blueprint_confidence,
)
from app.agents.workforce.engine import (
    WorkforceEngine,
)
from app.agents.workforce.prompts import (
    SYSTEM_PROMPT as WORKFORCE_SYSTEM_PROMPT,
    WORKFORCE_PROMPT,
)
from app.agents.workforce.validator import (
    validate as validate_workforce,
)
from app.agents.workforce.confidence import (
    calculate_confidence as calculate_workforce_confidence,
)
from app.agents.orchestrator.context import (
    OrchestrationContext,
)
from app.models.project import Project


def _get_project(
    db: Session,
    context: OrchestrationContext,
) -> Project:

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

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
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

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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

        technology_document = (
            context.technology.get(
                "technology_document"
            )
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the technology decisions document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
            "architecture": architecture_document,
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


def make_cost_adapter(
    db: Session,
):

    engine = CostEngine()

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
                "before cost estimation."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before cost estimation."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before cost estimation."
            )

        if not context.technology:
            raise ValueError(
                "Technology decisions are required "
                "before cost estimation."
            )

        if not context.database:
            raise ValueError(
                "Database design is required "
                "before cost estimation."
            )

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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

        technology_document = (
            context.technology.get(
                "technology_document"
            )
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the technology decisions document."
            )

        database_document = (
            context.database.get(
                "database_document"
            )
        )

        if not database_document:
            raise ValueError(
                "Database output does not contain "
                "the database design document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
            "architecture": architecture_document,
            "technology": technology_document,
            "database": database_document,
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
            "database_validation": (
                context.database.get(
                    "validation",
                    {},
                )
            ),
            "database_confidence": (
                context.database.get(
                    "confidence_score"
                )
            ),
        }

        document = engine.generate(
            system_prompt=COST_SYSTEM_PROMPT,
            section_prompt=COST_ESTIMATION_PROMPT,
            project_context=project_context,
        )

        validation = validate_cost(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_cost_confidence(
                validation
            )
        )

        return {
            "cost_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler


def make_critic_adapter(
    db: Session,
):

    engine = CriticEngine()

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
                "before Critic review."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before Critic review."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before Critic review."
            )

        if not context.technology:
            raise ValueError(
                "Technology decisions are required "
                "before Critic review."
            )

        if not context.database:
            raise ValueError(
                "Database design is required "
                "before Critic review."
            )

        if not context.cost:
            raise ValueError(
                "Cost estimation is required "
                "before Critic review."
            )

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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

        technology_document = (
            context.technology.get(
                "technology_document"
            )
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the technology decisions document."
            )

        database_document = (
            context.database.get(
                "database_document"
            )
        )

        if not database_document:
            raise ValueError(
                "Database output does not contain "
                "the database design document."
            )

        cost_document = (
            context.cost.get(
                "cost_document"
            )
        )

        if not cost_document:
            raise ValueError(
                "Cost output does not contain "
                "the cost estimation document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
            "architecture": architecture_document,
            "technology": technology_document,
            "database": database_document,
            "cost": cost_document,
        }

        document = engine.generate(
            system_prompt=CRITIC_SYSTEM_PROMPT,
            section_prompt=CRITIC_PROMPT,
            project_context=project_context,
        )

        validation = validate_critic(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_critic_confidence(
                validation
            )
        )

        return {
            "critic_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler


def make_blueprint_adapter(
    db: Session,
):

    engine = BlueprintEngine()

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
                "before Blueprint generation."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before Blueprint generation."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before Blueprint generation."
            )

        if not context.technology:
            raise ValueError(
                "Technology decisions are required "
                "before Blueprint generation."
            )

        if not context.database:
            raise ValueError(
                "Database design is required "
                "before Blueprint generation."
            )

        if not context.cost:
            raise ValueError(
                "Cost estimation is required "
                "before Blueprint generation."
            )

        if not context.critic:
            raise ValueError(
                "Critic review is required "
                "before Blueprint generation."
            )

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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

        technology_document = (
            context.technology.get(
                "technology_document"
            )
        )

        database_document = (
            context.database.get(
                "database_document"
            )
        )

        cost_document = (
            context.cost.get(
                "cost_document"
            )
        )

        critic_document = (
            context.critic.get(
                "critic_document"
            )
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the technology decisions document."
            )

        if not database_document:
            raise ValueError(
                "Database output does not contain "
                "the database design document."
            )

        if not cost_document:
            raise ValueError(
                "Cost output does not contain "
                "the cost estimation document."
            )

        if not critic_document:
            raise ValueError(
                "Critic output does not contain "
                "the critic document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
            "architecture": architecture_document,
            "technology": technology_document,
            "database": database_document,
            "cost": cost_document,
            "critic": critic_document,
        }

        document = engine.generate(
            system_prompt=BLUEPRINT_SYSTEM_PROMPT,
            section_prompt=BLUEPRINT_PROMPT,
            project_context=project_context,
        )

        validation = validate_blueprint(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_blueprint_confidence(
                validation
            )
        )

        return {
            "blueprint_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler


def make_workforce_adapter(
    db: Session,
):

    engine = WorkforceEngine()

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
                "before Workforce generation."
            )

        if not context.requirements:
            raise ValueError(
                "Requirements are required "
                "before Workforce generation."
            )

        if not context.architecture:
            raise ValueError(
                "Architecture is required "
                "before Workforce generation."
            )

        if not context.technology:
            raise ValueError(
                "Technology decisions are required "
                "before Workforce generation."
            )

        if not context.database:
            raise ValueError(
                "Database design is required "
                "before Workforce generation."
            )

        if not context.cost:
            raise ValueError(
                "Cost estimation is required "
                "before Workforce generation."
            )

        if not context.critic:
            raise ValueError(
                "Critic review is required "
                "before Workforce generation."
            )

        if not context.blueprint:
            raise ValueError(
                "Blueprint is required "
                "before Workforce generation."
            )

        architecture_record = (
            context.architecture.get(
                "architecture"
            )
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

        technology_document = (
            context.technology.get(
                "technology_document"
            )
        )

        database_document = (
            context.database.get(
                "database_document"
            )
        )

        cost_document = (
            context.cost.get(
                "cost_document"
            )
        )

        critic_document = (
            context.critic.get(
                "critic_document"
            )
        )

        blueprint_document = (
            context.blueprint.get(
                "blueprint_document"
            )
        )

        if not technology_document:
            raise ValueError(
                "Technology output does not contain "
                "the technology decisions document."
            )

        if not database_document:
            raise ValueError(
                "Database output does not contain "
                "the database design document."
            )

        if not cost_document:
            raise ValueError(
                "Cost output does not contain "
                "the cost estimation document."
            )

        if not critic_document:
            raise ValueError(
                "Critic output does not contain "
                "the critic document."
            )

        if not blueprint_document:
            raise ValueError(
                "Blueprint output does not contain "
                "the Blueprint document."
            )

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": context.discovery_memory,
            "requirements": context.requirements,
            "architecture": architecture_document,
            "technology": technology_document,
            "database": database_document,
            "cost": cost_document,
            "critic": critic_document,
            "blueprint": blueprint_document,
        }

        document = engine.generate(
            system_prompt=WORKFORCE_SYSTEM_PROMPT,
            section_prompt=WORKFORCE_PROMPT,
            project_context=project_context,
        )

        validation = validate_workforce(
            document=document,
            project_context=project_context,
        )

        confidence_score = (
            calculate_workforce_confidence(
                validation
            )
        )

        return {
            "workforce_document": document,
            "validation": validation,
            "confidence_score": confidence_score,
        }

    return handler
