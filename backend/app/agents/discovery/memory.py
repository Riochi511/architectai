from pydantic import BaseModel, Field

from app.agents.discovery.schemas import DiscoveryStage


class DiscoveryMemory(BaseModel):
    project_name: str | None = None

    vision: str | None = None

    primary_users: list[str] = Field(default_factory=list)

    secondary_users: list[str] = Field(default_factory=list)

    problem_statement: str | None = None

    functional_requirements: list[str] = Field(default_factory=list)

    non_functional_requirements: list[str] = Field(default_factory=list)

    ai_capabilities: list[str] = Field(default_factory=list)

    data_sources: list[str] = Field(default_factory=list)

    constraints: list[str] = Field(default_factory=list)

    deployment_target: str | None = None

    current_stage: DiscoveryStage = DiscoveryStage.VISION

    confidence_score: float = 0.0