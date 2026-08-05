def calculate_confidence(
    requirements: dict,
    validation: dict,
) -> int:
    """
    Calculates the overall quality score of the generated
    requirements.

    The score is deterministic.

    Maximum score = 100.
    """

    score = 0

    # --------------------------------------------------
    # Requirements Sections
    # --------------------------------------------------

    if requirements.get("business_requirements"):
        score += 10

    if requirements.get("functional_requirements"):
        score += 20

    if requirements.get("non_functional_requirements"):
        score += 15

    if requirements.get("business_rules"):
        score += 10

    if requirements.get("user_stories"):
        score += 10

    if requirements.get("acceptance_criteria"):
        score += 10

    if requirements.get("use_cases"):
        score += 10

    if requirements.get("constraints"):
        score += 5

    if requirements.get("risks"):
        score += 5

    if requirements.get("assumptions"):
        score += 5

    # --------------------------------------------------
    # Validation Penalties
    # --------------------------------------------------

    score -= len(validation.get("issues", [])) * 5

    score -= len(validation.get("warnings", [])) * 2

    score -= len(validation.get("missing_sections", [])) * 3

    score = max(score, 0)

    score = min(score, 100)

    return score