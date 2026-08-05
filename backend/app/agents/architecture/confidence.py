def calculate_confidence(validation: dict) -> int:
    """
    Calculates the overall confidence score
    for the generated Software Architecture Document.

    Returns an integer between 0 and 100.
    """

    score = 100

    # ----------------------------------
    # Deduct points for major issues
    # ----------------------------------

    score -= len(validation.get("issues", [])) * 10

    # ----------------------------------
    # Deduct points for warnings
    # ----------------------------------

    score -= len(validation.get("warnings", [])) * 3

    # ----------------------------------
    # Deduct points for missing sections
    # ----------------------------------

    score -= len(validation.get("missing_sections", [])) * 8

    # ----------------------------------
    # Deduct points for recommendations
    # ----------------------------------

    score -= len(validation.get("recommendations", []))

    # ----------------------------------
    # Never return below zero
    # ----------------------------------

    score = max(0, score)

    # ----------------------------------
    # Never exceed 100
    # ----------------------------------

    score = min(score, 100)

    return score