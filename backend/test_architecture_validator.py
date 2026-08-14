from app.database import SessionLocal
from app.models.project import Project
from app.models.architecture import Architecture
from app.agents.architecture.validator import validate
from app.agents.architecture.confidence import calculate_confidence


db = SessionLocal()

try:
    # HospitalFlow AI = project ID 5
    project = (
        db.query(Project)
        .filter(Project.id == 5)
        .first()
    )

    if not project:
        print("PROJECT NOT FOUND")
        raise SystemExit

    print(f"PROJECT: {project.name}")

    architecture = (
        db.query(Architecture)
        .filter(
            Architecture.project_id == project.id
        )
        .order_by(
            Architecture.id.desc()
        )
        .first()
    )

    if not architecture:
        print("ARCHITECTURE NOT FOUND")
        raise SystemExit

    print(f"ARCHITECTURE ID: {architecture.id}")
    print("Running architecture validator...")

    validation = validate(
        architecture.content
    )

    confidence = calculate_confidence(
        validation
    )

    print("\n" + "=" * 70)
    print("VALIDATION RESULT")
    print("=" * 70)

    print(f"VALID: {validation.get('valid')}")
    print(
        f"VALIDATOR CONFIDENCE: "
        f"{validation.get('confidence')}"
    )
    print(
        f"CALCULATED CONFIDENCE: "
        f"{confidence}"
    )

    print("\nISSUES:")
    for issue in validation.get("issues", []):
        print(f"- {issue}")

    print("\nWARNINGS:")
    for warning in validation.get("warnings", []):
        print(f"- {warning}")

    print("\nMISSING SECTIONS:")
    for section in validation.get(
        "missing_sections",
        [],
    ):
        print(f"- {section}")

    print("\nRECOMMENDATIONS:")
    for recommendation in validation.get(
        "recommendations",
        [],
    ):
        print(f"- {recommendation}")

    print("=" * 70)

finally:
    db.close()