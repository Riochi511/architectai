from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ArchitectureResponse(BaseModel):
    id: int
    title: str
    architecture_type: str
    content: str
    created_at: datetime
    project_id: int

    class Config:
        from_attributes = True


class ArchitectureGenerationResponse(BaseModel):
    architecture: ArchitectureResponse
    validation: dict[str, Any]
    confidence_score: int
    sections_generated: int
    generated_sections: list[str]