from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class OrchestrationContext:
    """
    Shared state passed between ArchitectAI orchestration stages.

    Each completed stage stores its output in the corresponding
    context field.

    Discovery remains interactive and is consumed as completed
    discovery memory.
    """

    project_id: int

    discovery_memory: dict[str, Any] | None = None

    requirements: dict[str, Any] | None = None

    architecture: dict[str, Any] | None = None

    technology: dict[str, Any] | None = None

    database: dict[str, Any] | None = None

    cost: dict[str, Any] | None = None

    critic: dict[str, Any] | None = None

    blueprint: dict[str, Any] | None = None

    workforce: dict[str, Any] | None = None

    workspace: dict[str, Any] | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

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

        elif stage == "workforce":
            self.workforce = output

        elif stage == "workspace":
            self.workspace = output

        else:
            raise ValueError(
                f"Unknown orchestration stage: {stage}"
            )
