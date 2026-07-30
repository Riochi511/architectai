from pydantic import BaseModel
from datetime import datetime


class ArchitectureResponse(BaseModel):
    id: int
    title: str
    architecture_type: str
    content: str
    created_at: datetime
    project_id: int

    class Config:
        from_attributes = True