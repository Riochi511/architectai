from pydantic import BaseModel


class RequirementCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str = "Medium"


class RequirementUpdate(BaseModel):
    title: str
    description: str
    category: str
    priority: str = "Medium"


class RequirementResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    project_id: int

    class Config:
        from_attributes = True