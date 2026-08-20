import asyncio
import time

import pytest

from app.agents.orchestrator.context import (
    OrchestrationContext,
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


@pytest.mark.asyncio
async def test_parallel_safe_agents_execute_concurrently():

    registry = AgentRegistry()

    start_times: dict[str, float] = {}

    async def discovery(context):
        return AgentResult.success(
            stage="discovery",
            output={},
        )

    async def requirements(context):
        return AgentResult.success(
            stage="requirements",
            output={
                "validation": {
                    "valid": True,
                }
            },
        )

    async def architecture(context):
        return AgentResult.success(
            stage="architecture",
            output={},
        )

    async def technology(context):

        start_times["technology"] = (
            time.perf_counter()
        )

        await asyncio.sleep(0.1)

        return AgentResult.success(
            stage="technology",
            output={},
        )

    async def database(context):

        start_times["database"] = (
            time.perf_counter()
        )

        await asyncio.sleep(0.1)

        return AgentResult.success(
            stage="database",
            output={},
        )

    async def cost(context):
        return AgentResult.success(
            stage="cost",
            output={},
        )

    async def critic(context):
        return AgentResult.success(
            stage="critic",
            output={
                "validation": {
                    "valid": True,
                }
            },
        )

    async def blueprint(context):
        return AgentResult.success(
            stage="blueprint",
            output={},
        )

    async def workspace(context):
        return AgentResult.success(
            stage="workspace",
            output={},
        )

    registry.register(
        "discovery",
        discovery,
    )

    registry.register(
        "requirements",
        requirements,
    )

    registry.register(
        "architecture",
        architecture,
    )

    registry.register(
        "technology",
        technology,
        parallel_safe=True,
    )

    registry.register(
        "database",
        database,
        parallel_safe=True,
    )

    registry.register(
        "cost",
        cost,
    )

    registry.register(
        "critic",
        critic,
    )

    registry.register(
        "blueprint",
        blueprint,
    )

    registry.register(
        "workspace",
        workspace,
    )

    def gate(context, result):
        return True

    orchestrator = Orchestrator(
        registry=registry,
        gates={
            "requirements": gate,
            "critic": gate,
        },
    )

    context = OrchestrationContext(
        project_id=1
    )

    started = time.perf_counter()

    await orchestrator.run(context)

    duration = (
        time.perf_counter()
        - started
    )

    assert "technology" in start_times
    assert "database" in start_times

    # Technology and Database each sleep for 100ms.
    # If they run sequentially, they would take roughly
    # 200ms. Parallel execution should complete faster.
    assert duration < 0.19

    # Their start times should be very close, proving
    # that they actually overlapped.
    assert abs(
        start_times["technology"]
        - start_times["database"]
    ) < 0.05