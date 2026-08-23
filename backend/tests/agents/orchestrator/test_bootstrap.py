from app.agents.orchestrator.bootstrap import (
    build_gates,
    build_registry,
)
from app.agents.orchestrator.registry import (
    AgentRegistry,
)


def test_build_registry_registers_active_agents():

    registry = build_registry(db=None)

    assert isinstance(
        registry,
        AgentRegistry,
    )

    assert registry.names() == [
        "discovery",
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]


def test_build_registry_registers_expected_handlers():

    registry = build_registry(db=None)

    assert registry.contains(
        "discovery"
    )

    assert registry.contains(
        "requirements"
    )

    assert registry.contains(
        "architecture"
    )

    assert registry.contains(
        "technology"
    )

    assert registry.contains(
        "database"
    )

    assert registry.contains(
        "cost"
    )

    assert registry.contains(
        "critic"
    )

    assert registry.contains(
        "blueprint"
    )

    assert registry.contains(
        "workforce"
    )


def test_build_gates_registers_requirements_gate():

    gates = build_gates()

    assert "requirements" in gates
    assert callable(
        gates["requirements"]
    )


def test_build_gates_does_not_register_future_gates():

    gates = build_gates()

    assert "critic" not in gates
    assert "blueprint" not in gates
    assert "workforce" not in gates
