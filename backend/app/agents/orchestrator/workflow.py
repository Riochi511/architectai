from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStage:
    """
    Defines one stage in the master ArchitectAI workflow.

    Discovery is intentionally excluded from this workflow
    because discovery is an interactive, multi-turn process
    handled by DiscoveryEngine and its API.

    The master orchestrator begins after discovery is complete.
    """

    name: str

    depends_on: tuple[str, ...] = ()

    gate_after: bool = False

    parallel_group: str | None = None


# ==========================================================
# MASTER ORCHESTRATION WORKFLOW
# ==========================================================

WORKFLOW: tuple[WorkflowStage, ...] = (

    # ------------------------------------------------------
    # Requirements
    # ------------------------------------------------------

    WorkflowStage(
        name="requirements",
        gate_after=True,
    ),

    # ------------------------------------------------------
    # Architecture
    # ------------------------------------------------------

    WorkflowStage(
        name="architecture",
        depends_on=("requirements",),
    ),
)


# ==========================================================
# WORKFLOW LOOKUP
# ==========================================================

WORKFLOW_BY_NAME = {
    stage.name: stage
    for stage in WORKFLOW
}