from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class WorkflowStage:

    name: str

    depends_on: tuple[str, ...] = ()

    gate_after: bool = False

    parallel_group: str | None = None


WORKFLOW = [

    WorkflowStage(
        name="discovery",
        depends_on=(),
        gate_after=False,
    ),

    WorkflowStage(
        name="requirements",
        depends_on=(
            "discovery",
        ),
        gate_after=True,
    ),

    WorkflowStage(
        name="architecture",
        depends_on=(
            "requirements",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="technology",
        depends_on=(
            "architecture",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="database",
        depends_on=(
            "technology",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="cost",
        depends_on=(
            "database",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="critic",
        depends_on=(
            "cost",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="blueprint",
        depends_on=(
            "critic",
        ),
        gate_after=False,
    ),

    WorkflowStage(
        name="workforce",
        depends_on=(
            "blueprint",
        ),
        gate_after=False,
    ),
]


WORKFLOW_BY_NAME = {
    stage.name: stage
    for stage in WORKFLOW
}