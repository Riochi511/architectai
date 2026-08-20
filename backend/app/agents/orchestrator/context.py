from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class OrchestrationContext:
    """
    Shared state flowing through the ArchitectAI workflow.

    The Orchestrator owns workflow state.
    Individual agents consume this context and return results.

    Agents should not mutate workflow state directly.
    """

    project_id: int | str

    discovery_memory: dict[str, Any] | None = None

    requirements: dict[str, Any] | None = None
    architecture: dict[str, Any] | None = None
    technology: dict[str, Any] | None = None
    database: dict[str, Any] | None = None
    cost: dict[str, Any] | None = None
    critic: dict[str, Any] | None = None
    blueprint: dict[str, Any] | None = None
    workspace: dict[str, Any] | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def set_stage_output(
        self,
        stage: str,
        output: dict[str, Any],
    ) -> None:
        """
        Store the output of a completed workflow stage.
        """

        if stage == "discovery":
            self.discovery_memory = output
        elif stage == "requirements":
            self.requirements = output
        elif stage == "architecture":
            self.architecture = output
        elif stage == "technology":
            self.technology = output
        elif stage == "database":
            self.database = output
        elif stage == "cost":
            self.cost = output
        elif stage == "critic":
            self.critic = output
        elif stage == "blueprint":
            self.blueprint = output
        elif stage == "workspace":
            self.workspace = output
        else:
            raise ValueError(
                f"Unknown orchestration stage: {stage}"
            )

    def get_stage_output(
        self,
        stage: str,
    ) -> dict[str, Any] | None:
        """
        Return the output associated with a workflow stage.
        """

        return {
            "discovery": self.discovery_memory,
            "requirements": self.requirements,
            "architecture": self.architecture,
            "technology": self.technology,
            "database": self.database,
            "cost": self.cost,
            "critic": self.critic,
            "blueprint": self.blueprint,
            "workspace": self.workspace,
        }.get(stage)