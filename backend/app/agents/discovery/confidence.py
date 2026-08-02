def calculate_confidence(memory: dict) -> int:
    score = 0

    if memory.get("vision"):
        score += 10

    if memory.get("users", {}).get("primary_users"):
        score += 10

    if memory.get("problem", {}).get("core_issues"):
        score += 15

    if memory.get("functional", {}).get("features"):
        score += 20

    if memory.get("non_functional", {}).get("requirements"):
        score += 15

    if memory.get("ai", {}).get("capabilities"):
        score += 10

    if memory.get("data", {}).get("sources"):
        score += 10

    if memory.get("constraints"):
        score += 5

    if memory.get("deployment"):
        score += 5

    return min(score, 100)