from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.agents.orchestrator.result import AgentResult


class WorkflowStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class OrchestrationState:

    project_id: int | str

    status: WorkflowStatus = WorkflowStatus.CREATED

    current_stage: str | None = None

    completed_stages: list[str] = field(
        default_factory=list
    )

    results: dict[str, AgentResult] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def record(
        self,
        result: AgentResult,
    ) -> None:

        self.results[result.stage] = result

        if result.succeeded:
            if result.stage not in self.completed_stages:
                self.completed_stages.append(
                    result.stage
                )

    def has_failed(self) -> bool:
        return any(
            result.failed
            for result in self.results.values()
        )