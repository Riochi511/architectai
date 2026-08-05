from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.requirement import Requirement
from app.models.architecture import Architecture

from app.agents.architecture.engine import ArchitectureEngine
from app.agents.architecture.registry import SECTION_REGISTRY
from app.agents.architecture.prompts import SYSTEM_PROMPT
from app.agents.architecture.compiler import ArchitectureCompiler
from app.agents.architecture.validator import validate
from app.agents.architecture.confidence import calculate_confidence


class ArchitectureOrchestrator:
    """
    Coordinates the complete Software Architecture
    generation workflow.
    """

    def generate(
        self,
        project: Project,
        db: Session,
    ) -> dict:

        # --------------------------------------------------
        # Load Project Requirements
        # --------------------------------------------------

        requirements = (
            db.query(Requirement)
            .filter(
                Requirement.project_id == project.id
            )
            .all()
        )

        # --------------------------------------------------
        # Build Project Context
        # --------------------------------------------------

        project_context = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            "discovery_memory": project.discovery_memory or {},
            "requirements": [
                {
                    "title": requirement.title,
                    "description": requirement.description,
                    "category": requirement.category,
                    "priority": requirement.priority,
                }
                for requirement in requirements
            ],
        }

        # --------------------------------------------------
        # Generate Architecture Sections
        # --------------------------------------------------

        engine = ArchitectureEngine()

        generated_sections = {}

        for section in SECTION_REGISTRY:

            print(f"Generating section: {section.title}")

            generated_sections[section.id] = engine.generate(
                system_prompt=SYSTEM_PROMPT,
                section_prompt=section.prompt,
                project_context=project_context,
            )

        # --------------------------------------------------
        # Compile Final Architecture Document
        # --------------------------------------------------

        compiler = ArchitectureCompiler()

        final_document = compiler.compile(
            generated_sections
        )

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        validation_report = validate(
            final_document
        )

        # --------------------------------------------------
        # Calculate Confidence
        # --------------------------------------------------

        confidence_score = calculate_confidence(
            validation_report
        )

        # --------------------------------------------------
        # Remove Existing Architecture (Optional)
        # Keep only the latest architecture per project.
        # --------------------------------------------------

        db.query(Architecture).filter(
            Architecture.project_id == project.id
        ).delete()

        # --------------------------------------------------
        # Save Architecture
        # --------------------------------------------------

        architecture = Architecture(
            title=f"{project.name} Architecture",
            architecture_type="System Architecture",
            content=final_document,
            project_id=project.id,
        )

        db.add(architecture)

        db.commit()

        db.refresh(architecture)

        # --------------------------------------------------
        # Return Result
        # --------------------------------------------------

        return {
            "architecture": architecture,
            "validation": validation_report,
            "confidence_score": confidence_score,
            "sections_generated": len(generated_sections),
            "generated_sections": list(generated_sections.keys()),
        }