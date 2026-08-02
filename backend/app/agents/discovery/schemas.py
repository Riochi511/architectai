from enum import Enum

from pydantic import BaseModel


class DiscoveryStage(str, Enum):
    VISION = "vision"
    USERS = "users"
    PROBLEM = "problem"
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    AI = "ai"
    DATA = "data"
    CONSTRAINTS = "constraints"
    DEPLOYMENT = "deployment"
    COMPLETE = "complete"


class DiscoveryRequest(BaseModel):
    project_id: int
    user_message: str


class DiscoveryResponse(BaseModel):
    next_question: str
    stage: DiscoveryStage
    confidence_score: float
    completed: bool