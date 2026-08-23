def calculate_confidence(
    validation: dict,
) -> int:
    """
    Calculates a deterministic Database Readiness score.

    The score measures how trustworthy and architecturally
    defensible the database design is.

    Maximum score = 100.
    """

    validator_confidence = validation.get(
        "confidence",
        100,
    )

    try:
        score = int(
            validator_confidence
        )
    except (TypeError, ValueError):
        score = 100

    issues = validation.get(
        "issues",
        [],
    )

    warnings = validation.get(
        "warnings",
        [],
    )

    missing_sections = validation.get(
        "missing_sections",
        [],
    )

    recommendations = validation.get(
        "recommendations",
        [],
    )

    score -= min(
        len(issues) * 10,
        50,
    )

    score -= min(
        len(warnings) * 3,
        15,
    )

    score -= min(
        len(missing_sections) * 8,
        32,
    )

    score -= min(
        len(recommendations),
        10,
    )

    if validation.get("valid") is False:
        score = min(
            score,
            59,
        )

    return max(
        0,
        min(score, 100),
    )