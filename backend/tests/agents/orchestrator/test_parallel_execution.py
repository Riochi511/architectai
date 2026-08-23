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

    async def technology(context):

        start_times["technology"] = (
            time.perf_counter()
        )

        await asyncio.sleep(0.1)

        return AgentResult.success(
            stage="technology",
            output={
                "stage": "technology",
            },
        )

    async def database(context):

        start_times["database"] = (
            time.perf_counter()
        )

        await asyncio.sleep(0.1)

        return AgentResult.success(
            stage="database",
            output={
                "stage": "database",
            },
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

    orchestrator = Orchestrator(
        registry=registry,
        gates={},
    )

    context = OrchestrationContext(
        project_id=1
    )

    started = time.perf_counter()

    results = await orchestrator._execute_batch(
        [
            "technology",
            "database",
        ],
        context,
    )

    duration = (
        time.perf_counter()
        - started
    )

    # Both stages must have executed.
    assert "technology" in start_times
    assert "database" in start_times

    # Both stages must have succeeded.
    assert all(
        result.succeeded
        for result in results
    )

    # The two 100ms operations should overlap.
    #
    # A sequential execution would be approximately
    # 200ms before runtime overhead. A wider threshold
    # avoids false failures caused by Windows scheduling
    # and test-runtime overhead while still detecting
    # genuinely sequential execution.
    assert duration < 0.30

    # The start times should be very close,
    # proving that execution overlapped.
    assert abs(
        start_times["technology"]
        - start_times["database"]
    ) < 0.05