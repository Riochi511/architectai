from fastapi.testclient import TestClient

from unittest.mock import patch

from app.agents.orchestrator.state import (
    OrchestrationState,
    WorkflowStatus,
)

from app.models import (
    Project,
    OrchestrationRun,
)


def make_successful_state(
    project_id: int,
):
    return OrchestrationState(
        project_id=project_id,
        status=WorkflowStatus.COMPLETED,
        current_stage=None,
        completed_stages=[
            "requirements",
            "architecture",
            "technology",
            "database",
            "cost",
            "critic",
            "blueprint",
            "workforce",
        ],
    )


class FakeOrchestrator:

    def __init__(
        self,
        state,
    ):
        self.state = state

    async def run(
        self,
        context,
    ):
        context.requirements = {
            "stage": "requirements",
        }

        context.architecture = {
            "stage": "architecture",
        }

        context.technology = {
            "stage": "technology",
        }

        context.database = {
            "stage": "database",
        }

        context.cost = {
            "stage": "cost",
        }

        context.critic = {
            "stage": "critic",
        }

        context.blueprint = {
            "stage": "blueprint",
        }

        context.workforce = {
            "stage": "workforce",
        }

        return self.state


def test_run_project_orchestration_returns_complete_pipeline(
    client: TestClient,
    db_session,
):
    project = Project(
        id=1,
        name="Test Project",
        description="Test project",
        owner_id=1,
    )

    db_session.add(project)
    db_session.commit()

    state = make_successful_state(
        project_id=1
    )

    with patch(
        "app.api.orchestration.build_orchestrator",
        return_value=FakeOrchestrator(
            state
        ),
    ):
        response = client.post(
            "/orchestration/run/1"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == 1
    assert data["run_id"] is not None
    assert data["status"] == "completed"

    assert data[
        "completed_stages"
    ] == [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]

    assert data["outputs"]["requirements"] == {
        "stage": "requirements",
    }

    assert data["outputs"]["architecture"] == {
        "stage": "architecture",
    }

    assert data["outputs"]["technology"] == {
        "stage": "technology",
    }

    assert data["outputs"]["database"] == {
        "stage": "database",
    }

    assert data["outputs"]["cost"] == {
        "stage": "cost",
    }

    assert data["outputs"]["critic"] == {
        "stage": "critic",
    }

    assert data["outputs"]["blueprint"] == {
        "stage": "blueprint",
    }

    assert data["outputs"]["workforce"] == {
        "stage": "workforce",
    }

    run = (
        db_session.query(
            OrchestrationRun
        )
        .filter(
            OrchestrationRun.id
            == data["run_id"]
        )
        .first()
    )

    assert run is not None
    assert run.project_id == 1
    assert run.status == "completed"
    assert run.error is None


def test_run_project_orchestration_returns_404_for_missing_project(
    client: TestClient,
):
    response = client.post(
        "/orchestration/run/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found.",
    }


def test_run_project_orchestration_rejects_project_owned_by_another_user(
    client: TestClient,
    db_session,
):
    project = Project(
        id=2,
        name="Other User Project",
        description="Private project",
        owner_id=999,
    )

    db_session.add(project)
    db_session.commit()

    response = client.post(
        "/orchestration/run/2"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found.",
    }

    run = (
        db_session.query(
            OrchestrationRun
        )
        .filter(
            OrchestrationRun.project_id
            == 2
        )
        .first()
    )

    assert run is None


def test_run_project_orchestration_handles_orchestrator_failure(
    client: TestClient,
    db_session,
):
    project = Project(
        id=3,
        name="Failing Project",
        description="Test failure",
        owner_id=1,
    )

    db_session.add(project)
    db_session.commit()

    class FailingOrchestrator:

        async def run(
            self,
            context,
        ):
            raise RuntimeError(
                "Orchestration failed internally"
            )

    with patch(
        "app.api.orchestration.build_orchestrator",
        return_value=FailingOrchestrator(),
    ):
        response = client.post(
            "/orchestration/run/3"
        )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Project orchestration failed.",
    }

    run = (
        db_session.query(
            OrchestrationRun
        )
        .filter(
            OrchestrationRun.project_id
            == 3
        )
        .order_by(
            OrchestrationRun.id.desc()
        )
        .first()
    )

    assert run is not None
    assert run.project_id == 3
    assert run.status == "failed"
    assert run.error == (
        "Orchestration failed internally"
    )


def test_get_orchestration_status_returns_latest_run(
    client: TestClient,
    db_session,
):
    project = Project(
        id=10,
        name="Status Project",
        description="Status test",
        owner_id=1,
    )

    db_session.add(project)
    db_session.commit()

    older_run = OrchestrationRun(
        project_id=10,
        status="failed",
        current_stage="technology",
        completed_stages=[
            "requirements",
            "architecture",
        ],
        results={},
        metadata_json={},
        error="Older failure",
    )

    latest_run = OrchestrationRun(
        project_id=10,
        status="completed",
        current_stage=None,
        completed_stages=[
            "requirements",
            "architecture",
            "technology",
            "database",
            "cost",
            "critic",
            "blueprint",
            "workforce",
        ],
        results={
            "workforce": {
                "stage": "workforce",
            },
        },
        metadata_json={
            "source": "test",
        },
        error=None,
    )

    db_session.add_all(
        [
            older_run,
            latest_run,
        ]
    )

    db_session.commit()

    response = client.get(
        "/orchestration/10/status"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == 10
    assert data["run_id"] == latest_run.id
    assert data["status"] == "completed"
    assert data["current_stage"] is None

    assert data[
        "completed_stages"
    ] == [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]

    assert data["error"] is None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_get_orchestration_status_returns_404_when_no_run_exists(
    client: TestClient,
    db_session,
):
    project = Project(
        id=11,
        name="No Run Project",
        description="No orchestration yet",
        owner_id=1,
    )

    db_session.add(project)
    db_session.commit()

    response = client.get(
        "/orchestration/11/status"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "No orchestration run found.",
    }


def test_get_orchestration_status_returns_404_for_missing_project(
    client: TestClient,
):
    response = client.get(
        "/orchestration/999/status"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found.",
    }


def test_get_orchestration_status_rejects_project_owned_by_another_user(
    client: TestClient,
    db_session,
):
    project = Project(
        id=12,
        name="Private Status Project",
        description="Private",
        owner_id=999,
    )

    db_session.add(project)
    db_session.commit()

    response = client.get(
        "/orchestration/12/status"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found.",
    }
