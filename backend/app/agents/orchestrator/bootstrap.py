from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.orchestrator.adapters import (
    make_architecture_adapter,
    make_discovery_adapter,
    make_requirements_adapter,
)
from app.agents.orchestrator.gates import (
    requirements_gate,
)
from app.agents.orchestrator.orchestrator import (
    Orchestrator,
)
from app.agents.orchestrator.registry import (
    AgentRegistry,
)


def build_registry(
    db: Session,
) -> AgentRegistry:
    """
    Build the central ArchitectAI agent registry.
    """

    registry = AgentRegistry()

    registry.register(
        "discovery",
        make_discovery_adapter(db),
    )

    registry.register(
        "requirements",
        make_requirements_adapter(db),
    )

    registry.register(
        "architecture",
        make_architecture_adapter(db),
    )

    return registry


def build_gates() -> dict:
    """
    Build quality gates for the active workflow.
    """

    return {
        "requirements": requirements_gate,
    }


def build_orchestrator(
    db: Session,
) -> Orchestrator:
    """
    Construct the application-level orchestrator.
    """

    return Orchestrator(
        registry=build_registry(db),
        gates=build_gates(),
    )