from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class OrchestrationOutputs(BaseModel):
    requirements: dict[str, Any] | None = None
    architecture: dict[str, Any] | None = None
    technology: dict[str, Any] | None = None
    database: dict[str, Any] | None = None
    cost: dict[str, Any] | None = None
    critic: dict[str, Any] | None = None
    blueprint: dict[str, Any] | None = None
    workforce: dict[str, Any] | None = None


class OrchestrationResponse(BaseModel):
    project_id: int
    status: str
    completed_stages: list[str]
    current_stage: str | None = None
    outputs: OrchestrationOutputs
