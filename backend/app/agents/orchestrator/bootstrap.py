from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.orchestrator.adapters import (
    make_architecture_adapter,
    make_blueprint_adapter,
    make_cost_adapter,
    make_critic_adapter,
    make_database_adapter,
    make_discovery_adapter,
    make_requirements_adapter,
    make_technology_adapter,
    make_workforce_adapter,
)
from app.agents.orchestrator.orchestrator import (
    Orchestrator,
)


def build_registry(
    db: Session,
):

    from app.agents.orchestrator.registry import (
        AgentRegistry,
    )

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

    registry.register(
        "technology",
        make_technology_adapter(db),
    )

    registry.register(
        "database",
        make_database_adapter(db),
    )

    registry.register(
        "cost",
        make_cost_adapter(db),
    )

    registry.register(
        "critic",
        make_critic_adapter(db),
    )

    registry.register(
        "blueprint",
        make_blueprint_adapter(db),
    )

    registry.register(
        "workforce",
        make_workforce_adapter(db),
    )

    return registry


def build_gates():

    def requirements_gate(
        context,
        result,
    ):

        output = result.output or {}

        validation = output.get(
            "validation",
            {},
        )

        return (
            validation.get(
                "valid",
                False,
            )
            is True
        )

    return {
        "requirements": requirements_gate,
    }


def build_orchestrator(
    db: Session,
) -> Orchestrator:

    return Orchestrator(
        registry=build_registry(db),
        gates=build_gates(),
    )
