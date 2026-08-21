import pytest

from app.agents.orchestrator.adapters import (
    make_discovery_adapter,
)
from app.agents.orchestrator.context import (
    OrchestrationContext,
)
from app.agents.discovery.schemas import (
    DiscoveryStage,
)
from app.models.project import Project


class FakeQuery:
    def __init__(self, project):
        self.project = project

    def filter(self, *args):
        return self

    def first(self):
        return self.project


class FakeDB:
    def __init__(self, project):
        self.project = project

    def query(self, model):
        return FakeQuery(self.project)


@pytest.mark.asyncio
async def test_discovery_adapter_returns_completed_memory():

    project = Project(
        id=1,
        name="Test Project",
        description="Test",
        owner_id=1,
        discovery_stage=DiscoveryStage.COMPLETE.value,
        discovery_memory={
            "vision": "Build an AI platform",
            "users": ["developers"],
        },
    )

    db = FakeDB(project)

    adapter = make_discovery_adapter(db)

    context = OrchestrationContext(
        project_id=1
    )

    result = await adapter(context)

    assert result == {
        "vision": "Build an AI platform",
        "users": ["developers"],
    }


@pytest.mark.asyncio
async def test_discovery_adapter_rejects_incomplete_discovery():

    project = Project(
        id=1,
        name="Test Project",
        description="Test",
        owner_id=1,
        discovery_stage=DiscoveryStage.VISION.value,
        discovery_memory={
            "vision": "Build an AI platform",
        },
    )

    db = FakeDB(project)

    adapter = make_discovery_adapter(db)

    context = OrchestrationContext(
        project_id=1
    )

    with pytest.raises(
        ValueError,
        match="Project discovery is not complete.",
    ):
        await adapter(context)


@pytest.mark.asyncio
async def test_discovery_adapter_rejects_missing_project():

    db = FakeDB(None)

    adapter = make_discovery_adapter(db)

    context = OrchestrationContext(
        project_id=999
    )

    with pytest.raises(
        ValueError,
        match="Project not found: 999",
    ):
        await adapter(context)