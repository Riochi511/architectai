def calculate_confidence(validation: dict) -> int:
    """
    Calculates the overall confidence score for the generated
    Software Architecture Document.

    The score reflects:
    - Validator confidence
    - Serious architectural issues
    - Warnings
    - Missing architecture sections
    - Recommendations

    Returns an integer between 0 and 100.
    """

    # --------------------------------------------------
    # Start from the validator's own confidence
    # --------------------------------------------------

    validator_confidence = validation.get(
        "confidence",
        100,
    )

    try:
        score = int(validator_confidence)
    except (TypeError, ValueError):
        score = 100

    # --------------------------------------------------
    # Major Issues
    #
    # Issues represent problems serious enough to
    # potentially prevent architecture approval.
    # --------------------------------------------------

    issues = validation.get(
        "issues",
        [],
    )

    score -= len(issues) * 10

    # --------------------------------------------------
    # Warnings
    #
    # Warnings indicate quality gaps but should have
    # less impact than architectural issues.
    # --------------------------------------------------

    warnings = validation.get(
        "warnings",
        [],
    )

    score -= len(warnings) * 3

    # --------------------------------------------------
    # Missing Sections
    #
    # Missing architecture sections are significant,
    # especially when they are required for approval.
    # --------------------------------------------------

    missing_sections = validation.get(
        "missing_sections",
        [],
    )

    score -= len(missing_sections) * 8

    # --------------------------------------------------
    # Recommendations
    #
    # Recommendations are normally improvement
    # opportunities, not architectural failures.
    #
    # Therefore they receive only a small deduction.
    # --------------------------------------------------

    recommendations = validation.get(
        "recommendations",
        [],
    )

    score -= len(recommendations)

    # --------------------------------------------------
    # Invalid Architecture Guard
    #
    # If the validator explicitly determines that the
    # architecture is invalid, confidence cannot remain
    # in the approval range.
    # --------------------------------------------------

    if validation.get("valid") is False:
        score = min(score, 59)

    # --------------------------------------------------
    # Valid Architecture Guard
    #
    # A valid architecture should not be penalized below
    # zero, regardless of the number of minor findings.
    # --------------------------------------------------

    score = max(
        0,
        score,
    )

    # --------------------------------------------------
    # Maximum Score
    # --------------------------------------------------

    score = min(
        100,
        score,
    )

    return score