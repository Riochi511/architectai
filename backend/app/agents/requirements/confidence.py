def calculate_confidence(
    requirements: dict,
    validation: dict,
) -> int:
    """
    Calculates a deterministic Requirements Readiness score.

    The score measures how defensible and architect-ready the
    generated requirements are.

    Maximum score = 100.
    """

    score = 100

    issues = validation.get("issues", [])
    warnings = validation.get("warnings", [])

    # --------------------------------------------------
    # Validation penalties
    # --------------------------------------------------

    score -= min(
        len(issues) * 15,
        45,
    )

    score -= min(
        len(warnings) * 3,
        15,
    )

    # --------------------------------------------------
    # Core requirement coverage
    # --------------------------------------------------

    if not requirements.get(
        "business_requirements"
    ):
        score -= 15

    if not requirements.get(
        "functional_requirements"
    ):
        score -= 20

    if not requirements.get(
        "non_functional_requirements"
    ):
        score -= 15

    # --------------------------------------------------
    # Supporting artifacts
    #
    # These improve readiness but are not universally
    # required for every project.
    # --------------------------------------------------

    if not requirements.get(
        "acceptance_criteria"
    ):
        score -= 4

    if not requirements.get(
        "use_cases"
    ):
        score -= 2

    if not requirements.get(
        "risks"
    ):
        score -= 3

    # --------------------------------------------------
    # Open questions
    #
    # Unknowns are not automatically defects.
    # They only reduce readiness when several material
    # questions remain unresolved.
    # --------------------------------------------------

    open_questions = requirements.get(
        "open_questions",
        [],
    )

    if len(open_questions) >= 6:
        score -= 10

    elif len(open_questions) >= 4:
        score -= 6

    elif len(open_questions) >= 2:
        score -= 3

    # --------------------------------------------------
    # Assumptions
    #
    # A small number of explicit assumptions is acceptable.
    # Excessive assumptions indicate unresolved discovery.
    # --------------------------------------------------

    assumptions = requirements.get(
        "assumptions",
        [],
    )

    if len(assumptions) >= 5:
        score -= 6

    elif len(assumptions) >= 3:
        score -= 3

    # --------------------------------------------------
    # Clamp
    # --------------------------------------------------

    return max(
        0,
        min(score, 100),
    )