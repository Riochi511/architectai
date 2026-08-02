from app.agents.discovery.memory import DiscoveryMemory


def calculate_confidence(memory: DiscoveryMemory) -> float:
    completed = 0
    total = 9

    if memory.vision:
        completed += 1

    if memory.primary_users:
        completed += 1

    if memory.problem_statement:
        completed += 1

    if memory.functional_requirements:
        completed += 1

    if memory.non_functional_requirements:
        completed += 1

    if memory.ai_capabilities:
        completed += 1

    if memory.data_sources:
        completed += 1

    if memory.constraints:
        completed += 1

    if memory.deployment_target:
        completed += 1

    return round(completed / total, 2)