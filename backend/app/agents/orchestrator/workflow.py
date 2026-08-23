from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStage:
    """
    Defines one stage in the master ArchitectAI workflow.

    Discovery is intentionally excluded because it is an
    interactive multi-turn process handled separately.

    The master workflow begins after discovery is complete.
    """

    name: str

    depends_on: tuple[str, ...] = ()

    gate_after: bool = False

    parallel_group: str | None = None


WORKFLOW: tuple[WorkflowStage, ...] = (

    WorkflowStage(
        name="requirements",
        gate_after=True,
    ),

    WorkflowStage(
        name="architecture",
        depends_on=("requirements",),
    ),

    WorkflowStage(
        name="technology",
        depends_on=("architecture",),
    ),

    WorkflowStage(
        name="database",
        depends_on=("technology",),
    ),

    WorkflowStage(
        name="cost",
        depends_on=("database",),
    ),

    WorkflowStage(
        name="critic",
        depends_on=("cost",),
    ),

    WorkflowStage(
        name="blueprint",
        depends_on=("critic",),
    ),
)


WORKFLOW_BY_NAME = {
    stage.name: stage
    for stage in WORKFLOW
}
