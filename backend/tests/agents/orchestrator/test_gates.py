from app.agents.orchestrator.context import (
    OrchestrationContext,
)

from app.agents.orchestrator.gates import (
    critic_gate,
    requirements_gate,
)

from app.agents.orchestrator.result import (
    AgentResult,
)


def test_requirements_gate_passes_valid_requirements():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="requirements",
        output={
            "requirements": {},
            "validation": {
                "valid": True,
            },
        },
    )

    assert requirements_gate(
        context,
        result,
    ) is True


def test_requirements_gate_rejects_invalid_requirements():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="requirements",
        output={
            "requirements": {},
            "validation": {
                "valid": False,
            },
        },
    )

    assert requirements_gate(
        context,
        result,
    ) is False


def test_requirements_gate_rejects_failed_agent():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.failure(
        stage="requirements",
        error="Requirements generation failed",
    )

    assert requirements_gate(
        context,
        result,
    ) is False


def test_critic_gate_accepts_valid_validation():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="critic",
        output={
            "validation": {
                "valid": True,
            },
        },
    )

    assert critic_gate(
        context,
        result,
    ) is True


def test_critic_gate_rejects_invalid_validation():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="critic",
        output={
            "validation": {
                "valid": False,
            },
        },
    )

    assert critic_gate(
        context,
        result,
    ) is False


def test_critic_gate_accepts_approved_result():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="critic",
        output={
            "approved": True,
        },
    )

    assert critic_gate(
        context,
        result,
    ) is True


def test_critic_gate_rejects_missing_decision():
    context = OrchestrationContext(
        project_id=1
    )

    result = AgentResult.success(
        stage="critic",
        output={},
    )

    assert critic_gate(
        context,
        result,
    ) is False