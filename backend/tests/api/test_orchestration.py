from unittest.mock import patch

from app.models import Project


class FakeOrchestrationState:

    status = "completed"

    completed_stages = [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]

    current_stage = None


class FakeOrchestrator:

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

        return FakeOrchestrationState()


def test_run_project_orchestration_returns_complete_pipeline(
    client,
    db_session,
):
    project = Project(
        id=1,
        name="Test Project",
        description="Test orchestration",
        owner_id=1,
    )

    db_session.add(project)
    db_session.commit()

    with patch(
        "app.api.orchestration.build_orchestrator",
        return_value=FakeOrchestrator(),
    ):

        response = client.post(
            "/orchestration/run/1"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == 1

    assert data["status"] == "completed"

    assert data["completed_stages"] == [
        "requirements",
        "architecture",
        "technology",
        "database",
        "cost",
        "critic",
        "blueprint",
        "workforce",
    ]

    assert data["current_stage"] is None

    assert "outputs" in data

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


def test_run_project_orchestration_returns_404_for_missing_project(
    client,
):
    response = client.post(
        "/orchestration/run/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found."
    }


def test_run_project_orchestration_rejects_project_owned_by_another_user(
    client,
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
        "detail": "Project not found."
    }


def test_run_project_orchestration_handles_orchestrator_failure(
    client,
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
        "detail": "Project orchestration failed."
    }

    assert (
        "Orchestration failed internally"
        not in response.text
    )
