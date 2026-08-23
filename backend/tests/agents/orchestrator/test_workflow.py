from app.agents.orchestrator.workflow import (
    WORKFLOW,
    WORKFLOW_BY_NAME,
)


def test_workflow_contains_expected_stages():
    stages = [
        stage.name
        for stage in WORKFLOW
    ]

    assert stages == [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
    ]


def test_requirements_is_the_first_master_stage():
    assert WORKFLOW_BY_NAME[
        "requirements"
    ].depends_on == ()


def test_requirements_requires_quality_gate():
    assert WORKFLOW_BY_NAME[
        "requirements"
    ].gate_after is True


def test_architecture_depends_on_requirements():
    assert WORKFLOW_BY_NAME[
        "architecture"
    ].depends_on == (
        "requirements",
    )


def test_architecture_does_not_require_quality_gate():
    assert WORKFLOW_BY_NAME[
        "architecture"
    ].gate_after is False


def test_technology_depends_on_architecture():
    assert WORKFLOW_BY_NAME[
        "technology"
    ].depends_on == (
        "architecture",
    )


def test_database_depends_on_technology():
    assert WORKFLOW_BY_NAME[
        "database"
    ].depends_on == (
        "technology",
    )


def test_cost_depends_on_database():
    assert WORKFLOW_BY_NAME[
        "cost"
    ].depends_on == (
        "database",
    )


def test_critic_depends_on_cost():
    assert WORKFLOW_BY_NAME[
        "critic"
    ].depends_on == (
        "cost",
    )


def test_blueprint_depends_on_critic():
    assert WORKFLOW_BY_NAME[
        "blueprint"
    ].depends_on == (
        "critic",
    )


def test_critic_does_not_require_quality_gate():
    assert WORKFLOW_BY_NAME[
        "critic"
    ].gate_after is False


def test_blueprint_does_not_require_quality_gate():
    assert WORKFLOW_BY_NAME[
        "blueprint"
    ].gate_after is False


def test_workflow_does_not_include_interactive_discovery():
    assert "discovery" not in WORKFLOW_BY_NAME


def test_workflow_does_not_include_unimplemented_future_stages():
    future_stages = {
        "workspace",
    }

    assert future_stages.isdisjoint(
        WORKFLOW_BY_NAME
    )
