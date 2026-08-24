from __future__ import annotations

import asyncio
import inspect
import time
from typing import Callable

from app.agents.orchestrator.context import (
    OrchestrationContext,
)
from app.agents.orchestrator.exceptions import (
    AgentNotRegisteredError,
    GateFailedError,
    WorkflowDefinitionError,
)
from app.agents.orchestrator.registry import (
    AgentRegistry,
)
from app.agents.orchestrator.result import (
    AgentResult,
)
from app.agents.orchestrator.state import (
    OrchestrationState,
    WorkflowStatus,
)
from app.agents.orchestrator.workflow import (
    WORKFLOW,
    WORKFLOW_BY_NAME,
)


GateCallable = Callable[
    [OrchestrationContext, AgentResult],
    bool | None,
]


class Orchestrator:
    """
    Deterministic workflow controller for ArchitectAI.

    Responsibilities:

    - enforce workflow ordering
    - execute registered agents
    - enforce quality gates
    - execute explicitly parallel-safe stages concurrently
    - aggregate results
    - stop execution on required failures

    The Orchestrator does not make architectural decisions.
    """

    def __init__(
        self,
        registry: AgentRegistry,
        gates: dict[str, GateCallable] | None = None,
    ) -> None:

        self.registry = registry
        self.gates = gates or {}

        self._validate_workflow()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    async def run(
        self,
        context: OrchestrationContext,
    ) -> OrchestrationState:

        state = OrchestrationState(
            project_id=context.project_id
        )

        state.status = WorkflowStatus.RUNNING
        state.current_stage = None

        try:

            completed: set[str] = set()

            while len(completed) < len(WORKFLOW):

                ready = self._get_ready_stages(
                    completed
                )

                if not ready:
                    raise WorkflowDefinitionError(
                        "Workflow contains unresolved "
                        "dependencies or a cycle."
                    )

                batches = self._build_execution_batch(
                    ready
                )

                for batch in batches:

                    # --------------------------------------------------
                    # Track the stage currently being executed.
                    #
                    # For a parallel batch, expose the first stage as
                    # the current stage while all stages in the batch
                    # execute concurrently.
                    # --------------------------------------------------

                    state.current_stage = (
                        batch[0]
                        if batch
                        else None
                    )

                    results = await self._execute_batch(
                        batch=batch,
                        context=context,
                    )

                    for result in results:

                        state.record(result)

                        if result.failed:

                            stage = WORKFLOW_BY_NAME[
                                result.stage
                            ]

                            if stage.gate_after:
                                raise GateFailedError(
                                    f"Stage failed: "
                                    f"{result.stage}: "
                                    f"{result.error}"
                                )

                            spec = self.registry.get(
                                result.stage
                            )

                            if spec.required:
                                raise GateFailedError(
                                    f"Required stage failed: "
                                    f"{result.stage}: "
                                    f"{result.error}"
                                )

                            # Optional failed stages are recorded
                            # but are not considered completed.
                            continue

                        if result.succeeded:

                            if result.output:
                                context.set_stage_output(
                                    result.stage,
                                    result.output,
                                )

                            completed.add(
                                result.stage
                            )

                            await self._run_gate(
                                result.stage,
                                context,
                                result,
                            )

                    # --------------------------------------------------
                    # If the batch completed successfully, clear the
                    # current stage before moving to the next batch.
                    # --------------------------------------------------

                    state.current_stage = None

            state.current_stage = None
            state.status = WorkflowStatus.COMPLETED

            return state

        except Exception:

            state.status = WorkflowStatus.FAILED

            raise

    # --------------------------------------------------
    # Workflow validation
    # --------------------------------------------------

    def _validate_workflow(self) -> None:

        names = {
            stage.name
            for stage in WORKFLOW
        }

        for stage in WORKFLOW:

            for dependency in stage.depends_on:

                if dependency not in names:
                    raise WorkflowDefinitionError(
                        f"Stage '{stage.name}' depends "
                        f"on unknown stage "
                        f"'{dependency}'."
                    )

        # --------------------------------------------------
        # Simple cycle detection.
        # --------------------------------------------------

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(name: str) -> None:

            if name in visiting:
                raise WorkflowDefinitionError(
                    "Workflow contains a dependency cycle."
                )

            if name in visited:
                return

            visiting.add(name)

            for dependency in WORKFLOW_BY_NAME[
                name
            ].depends_on:

                visit(dependency)

            visiting.remove(name)
            visited.add(name)

        for name in names:
            visit(name)

    # --------------------------------------------------
    # Dependency resolution
    # --------------------------------------------------

    def _get_ready_stages(
        self,
        completed: set[str],
    ) -> list[str]:

        ready: list[str] = []

        for stage in WORKFLOW:

            if stage.name in completed:
                continue

            if all(
                dependency in completed
                for dependency in stage.depends_on
            ):
                ready.append(stage.name)

        return ready

    # --------------------------------------------------
    # Batch construction
    # --------------------------------------------------

    def _build_execution_batch(
        self,
        ready: list[str],
    ) -> list[list[str]]:

        parallel_groups: dict[
            str,
            list[str],
        ] = {}

        sequential: list[str] = []

        for name in ready:

            stage = WORKFLOW_BY_NAME[name]

            if stage.parallel_group:

                parallel_groups.setdefault(
                    stage.parallel_group,
                    [],
                ).append(name)

            else:

                sequential.append(name)

        batches: list[list[str]] = []

        # --------------------------------------------------
        # Sequential stages.
        # --------------------------------------------------

        for name in sequential:
            batches.append([name])

        # --------------------------------------------------
        # Explicitly parallel-safe groups.
        # --------------------------------------------------

        for group in parallel_groups.values():

            if len(group) == 1:

                batches.append(group)

                continue

            if all(
                self.registry.get(
                    name
                ).parallel_safe
                for name in group
            ):

                batches.append(group)

            else:

                for name in group:
                    batches.append([name])

        return batches

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    async def _execute_batch(
        self,
        batch: list[str],
        context: OrchestrationContext,
    ) -> list[AgentResult]:

        if len(batch) == 1:

            return [
                await self._execute_stage(
                    batch[0],
                    context,
                )
            ]

        results = await asyncio.gather(
            *(
                self._execute_stage(
                    stage,
                    context,
                )
                for stage in batch
            )
        )

        return list(results)

    async def _execute_stage(
        self,
        stage: str,
        context: OrchestrationContext,
    ) -> AgentResult:

        if not self.registry.contains(stage):

            raise AgentNotRegisteredError(
                f"No agent registered for stage "
                f"'{stage}'."
            )

        started = time.perf_counter()

        print()
        print("=" * 80)
        print(
            f"ORCHESTRATOR: Starting stage "
            f"'{stage}'"
        )
        print("=" * 80)

        try:

            result = await self.registry.execute(
                stage,
                context,
            )

            duration_ms = (
                time.perf_counter()
                - started
            ) * 1000

            result.duration_ms = duration_ms

            print()
            print("=" * 80)
            print(
                f"ORCHESTRATOR: Stage "
                f"'{stage}' completed successfully"
            )
            print(
                f"ORCHESTRATOR: Duration: "
                f"{duration_ms:.2f} ms"
            )
            print("=" * 80)

            return result

        except Exception as exc:

            duration_ms = (
                time.perf_counter()
                - started
            ) * 1000

            print()
            print("=" * 80)
            print(
                f"ORCHESTRATOR: STAGE "
                f"'{stage}' FAILED"
            )
            print(
                f"Exception Type: "
                f"{type(exc).__name__}"
            )
            print(
                f"Exception: {exc}"
            )
            print(
                f"Duration: "
                f"{duration_ms:.2f} ms"
            )
            print()
            print("TRACEBACK")
            print("-" * 80)

            import traceback

            traceback.print_exc()

            print("=" * 80)

            return AgentResult.failure(
                stage=stage,
                error=(
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
                duration_ms=duration_ms,
            )

    # --------------------------------------------------
    # Gates
    # --------------------------------------------------

    async def _run_gate(
        self,
        stage: str,
        context: OrchestrationContext,
        result: AgentResult,
    ) -> None:

        workflow_stage = WORKFLOW_BY_NAME[
            stage
        ]

        if not workflow_stage.gate_after:
            return

        gate = self.gates.get(stage)

        if gate is None:
            raise GateFailedError(
                f"Stage '{stage}' requires a quality "
                f"gate, but no gate is registered."
            )

        outcome = gate(
            context,
            result,
        )

        if inspect.isawaitable(outcome):
            outcome = await outcome

        if outcome is False:
            raise GateFailedError(
                f"Quality gate failed after "
                f"stage '{stage}'."
            )