from sqlalchemy.orm import Session

from app.agents.requirements.confidence import calculate_confidence
from app.agents.requirements.extractor import extract
from app.agents.requirements.validator import validate

from app.models.project import Project
from app.models.requirement import Requirement


class RequirementsEngine:

    def process(
        self,
        project: Project,
        db: Session,
    ) -> dict:
        """
        Generates structured software requirements
        from the completed discovery memory.
        """

        discovery_memory = project.discovery_memory or {}

        # ----------------------------------------
        # Step 1
        # Extract Requirements
        # ----------------------------------------

        requirements = extract(discovery_memory)

        # Preserve the complete rich requirements
        # document on the project.
        project.requirements_document = requirements

        # ----------------------------------------
        # Step 2
        # Validate Requirements
        # ----------------------------------------

        validation = validate(
            requirements=requirements,
            discovery_memory=discovery_memory,
        )

        # ----------------------------------------
        # Step 3
        # Calculate Confidence
        # ----------------------------------------

        confidence = calculate_confidence(
            requirements=requirements,
            validation=validation,
        )

        # ----------------------------------------
        # Step 4
        # Remove Existing Requirements
        # ----------------------------------------

        (
            db.query(Requirement)
            .filter(
                Requirement.project_id == project.id
            )
            .delete()
        )

        # Apply deletion before inserting new rows.
        db.flush()

        # ----------------------------------------
        # Step 5
        # Save Business Requirements
        # ----------------------------------------

        for item in requirements.get(
            "business_requirements",
            [],
        ):
            db.add(
                Requirement(
                    title=item["title"],
                    description=item["description"],
                    category="Business",
                    priority=item.get(
                        "priority",
                        "Medium",
                    ),
                    project_id=project.id,
                )
            )

        # ----------------------------------------
        # Step 6
        # Save Functional Requirements
        # ----------------------------------------

        for item in requirements.get(
            "functional_requirements",
            [],
        ):
            db.add(
                Requirement(
                    title=item["title"],
                    description=item["description"],
                    category="Functional",
                    priority=item.get(
                        "priority",
                        "Medium",
                    ),
                    project_id=project.id,
                )
            )

        # ----------------------------------------
        # Step 7
        # Save Non-Functional Requirements
        # ----------------------------------------

        for item in requirements.get(
            "non_functional_requirements",
            [],
        ):
            db.add(
                Requirement(
                    title=item["title"],
                    description=item["description"],
                    category="Non Functional",
                    priority=item.get(
                        "priority",
                        "Medium",
                    ),
                    project_id=project.id,
                )
            )

        # ----------------------------------------
        # Step 8
        # Commit Changes
        # ----------------------------------------

        db.commit()

        # Refresh the project so relationships
        # reflect the latest database state.
        db.refresh(project)

        # ----------------------------------------
        # Step 9
        # Return Result
        # ----------------------------------------

        return {
            "requirements": requirements,
            "validation": validation,
            "confidence_score": confidence,
            "requirements_generated": len(project.requirements),
        }