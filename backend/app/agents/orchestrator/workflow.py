from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStage:
    name: str

    depends_on: tuple[str, ...] = ()

    gate_after: bool = False

    parallel_group: str | None = None


WORKFLOW: tuple[WorkflowStage, ...] = (

    WorkflowStage(
        name="discovery",
    ),

    WorkflowStage(
        name="requirements",
        depends_on=("discovery",),
        gate_after=True,
    ),

    WorkflowStage(
        name="architecture",
        depends_on=("requirements",),
    ),

    WorkflowStage(
        name="technology",
        depends_on=("architecture",),
        parallel_group="architecture_outputs",
    ),

    WorkflowStage(
        name="database",
        depends_on=("architecture",),
        parallel_group="architecture_outputs",
    ),

    WorkflowStage(
        name="cost",
        depends_on=(
            "technology",
            "database",
        ),
    ),

    WorkflowStage(
        name="critic",
        depends_on=("cost",),
        gate_after=True,
    ),

    WorkflowStage(
        name="blueprint",
        depends_on=("critic",),
    ),

    WorkflowStage(
        name="workspace",
        depends_on=("blueprint",),
    ),
)


WORKFLOW_BY_NAME = {
    stage.name: stage
    for stage in WORKFLOW
}