from app.agents.orchestrator.workflow import (
    WORKFLOW,
    WORKFLOW_BY_NAME,
)


def test_workflow_contains_expected_stages():
    stages = [stage.name for stage in WORKFLOW]

    assert stages == [
        "discovery",
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workspace",
    ]


def test_requirements_depends_on_discovery():
    assert WORKFLOW_BY_NAME[
        "requirements"
    ].depends_on == ("discovery",)


def test_architecture_depends_on_requirements():
    assert WORKFLOW_BY_NAME[
        "architecture"
    ].depends_on == ("requirements",)


def test_technology_and_database_depend_on_architecture():
    assert WORKFLOW_BY_NAME[
        "technology"
    ].depends_on == ("architecture",)

    assert WORKFLOW_BY_NAME[
        "database"
    ].depends_on == ("architecture",)


def test_cost_waits_for_technology_and_database():
    assert WORKFLOW_BY_NAME[
        "cost"
    ].depends_on == (
        "technology",
        "database",
    )


def test_critic_depends_on_cost():
    assert WORKFLOW_BY_NAME[
        "critic"
    ].depends_on == ("cost",)


def test_blueprint_depends_on_critic():
    assert WORKFLOW_BY_NAME[
        "blueprint"
    ].depends_on == ("critic",)


def test_workspace_depends_on_blueprint():
    assert WORKFLOW_BY_NAME[
        "workspace"
    ].depends_on == ("blueprint",)


def test_quality_gates_are_at_correct_stages():
    assert WORKFLOW_BY_NAME[
        "requirements"
    ].gate_after is True

    assert WORKFLOW_BY_NAME[
        "critic"
    ].gate_after is True