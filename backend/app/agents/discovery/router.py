from fastapi import APIRouter

from app.agents.discovery.engine import DiscoveryEngine
from app.agents.discovery.schemas import DiscoveryRequest

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"],
)

engine = DiscoveryEngine()


@router.post("/start")
def start_discovery(request: DiscoveryRequest):

    result = engine.process(request.user_message)

    return {
        "next_question": result["question"],
        "stage": engine.memory.current_stage,
        "confidence_score": engine.memory.confidence_score,
        "completed": result["completed"],
    }