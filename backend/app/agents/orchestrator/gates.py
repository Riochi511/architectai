from app.agents.orchestrator.context import (
    OrchestrationContext,
)

from app.agents.orchestrator.result import (
    AgentResult,
)


def requirements_gate(
    context: OrchestrationContext,
    result: AgentResult,
) -> bool:

    if not result.succeeded:
        return False

    output = result.output or {}

    validation = output.get(
        "validation",
        {},
    )

    return validation.get(
        "valid",
        False,
    ) is True


def critic_gate(
    context: OrchestrationContext,
    result: AgentResult,
) -> bool:

    if not result.succeeded:
        return False

    output = result.output or {}

    validation = output.get(
        "validation",
        {},
    )

    if "valid" in validation:
        return validation["valid"] is True

    if "approved" in output:
        return output["approved"] is True

    return False