import pytest

from app.agents.orchestrator.context import (
    OrchestrationContext,
)

from app.agents.orchestrator.exceptions import (
    GateFailedError,
)

from app.agents.orchestrator.orchestrator import (
    Orchestrator,
)

from app.agents.orchestrator.registry import (
    AgentRegistry,
)

from app.agents.orchestrator.result import (
    AgentResult,
)

from app.agents.orchestrator.state import (
    WorkflowStatus,
)


def make_registry(
    *,
    fail_stage: str | None = None,
) -> AgentRegistry:

    registry = AgentRegistry()

    stages = [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]

    for stage in stages:

        async def current_handler(
            context,
            _stage=stage,
        ):

            if _stage == fail_stage:

                return AgentResult.failure(
                    stage=_stage,
                    error=f"{_stage} failed",
                )

            output = {
                "stage": _stage,
            }

            if _stage == "requirements":

                output["validation"] = {
                    "valid": True,
                }

            return AgentResult.success(
                stage=_stage,
                output=output,
            )

        registry.register(
            stage,
            current_handler,
        )

    return registry


def make_gates():

    def requirements_gate(
        context,
        result,
    ):

        output = result.output or {}

        validation = output.get(
            "validation",
            {},
        )

        return (
            validation.get(
                "valid",
                False,
            )
            is True
        )

    return {
        "requirements": requirements_gate,
    }


@pytest.mark.asyncio
async def test_orchestrator_completes_workflow():

    registry = make_registry()

    orchestrator = Orchestrator(
        registry=registry,
        gates=make_gates(),
    )

    context = OrchestrationContext(
        project_id=1
    )

    state = await orchestrator.run(
        context
    )

    assert state.status == (
        WorkflowStatus.COMPLETED
    )

    assert state.completed_stages == [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]


@pytest.mark.asyncio
async def test_orchestrator_stops_when_required_stage_fails():

    registry = make_registry(
        fail_stage="architecture"
    )

    orchestrator = Orchestrator(
        registry=registry,
        gates=make_gates(),
    )

    context = OrchestrationContext(
        project_id=1
    )

    with pytest.raises(
        GateFailedError
    ):

        await orchestrator.run(
            context
        )


@pytest.mark.asyncio
async def test_context_receives_stage_outputs():

    registry = make_registry()

    orchestrator = Orchestrator(
        registry=registry,
        gates=make_gates(),
    )

    context = OrchestrationContext(
        project_id=42
    )

    state = await orchestrator.run(
        context
    )

    assert state.status == (
        WorkflowStatus.COMPLETED
    )

    assert context.discovery_memory is None

    assert context.requirements[
        "stage"
    ] == "requirements"

    assert context.architecture[
        "stage"
    ] == "architecture"

    assert context.technology[
        "stage"
    ] == "technology"

    assert context.database[
        "stage"
    ] == "database"

    assert context.cost[
        "stage"
    ] == "cost"

    assert context.critic[
        "stage"
    ] == "critic"

    assert context.blueprint[
        "stage"
    ] == "blueprint"

    assert context.workforce[
        "stage"
    ] == "workforce"

    assert context.workspace is None


@pytest.mark.asyncio
async def test_requirements_gate_blocks_workflow():

    registry = make_registry()

    def failing_requirements_gate(
        context,
        result,
    ):

        return False

    orchestrator = Orchestrator(
        registry=registry,
        gates={
            "requirements":
                failing_requirements_gate,
        },
    )

    context = OrchestrationContext(
        project_id=1
    )

    with pytest.raises(
        GateFailedError
    ):

        await orchestrator.run(
            context
        )

    assert context.requirements is not None
    assert context.architecture is None
    assert context.technology is None
    assert context.database is None
    assert context.cost is None
    assert context.critic is None
    assert context.blueprint is None
    assert context.workforce is None
