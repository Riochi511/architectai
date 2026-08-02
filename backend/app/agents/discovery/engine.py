from app.agents.discovery.confidence import calculate_confidence
from app.agents.discovery.interviewer import ask
from app.agents.discovery.refiner import refine
from app.agents.discovery.schemas import DiscoveryStage


class DiscoveryEngine:

    STAGE_FLOW = {
        DiscoveryStage.VISION: DiscoveryStage.USERS,
        DiscoveryStage.USERS: DiscoveryStage.PROBLEM,
        DiscoveryStage.PROBLEM: DiscoveryStage.FUNCTIONAL,
        DiscoveryStage.FUNCTIONAL: DiscoveryStage.NON_FUNCTIONAL,
        DiscoveryStage.NON_FUNCTIONAL: DiscoveryStage.AI,
        DiscoveryStage.AI: DiscoveryStage.DATA,
        DiscoveryStage.DATA: DiscoveryStage.CONSTRAINTS,
        DiscoveryStage.CONSTRAINTS: DiscoveryStage.DEPLOYMENT,
        DiscoveryStage.DEPLOYMENT: DiscoveryStage.COMPLETE,
    }

    def process(self, project, user_message: str | None = None):

        memory = project.discovery_memory or {}

        stage = project.discovery_stage or DiscoveryStage.VISION

        if isinstance(stage, str):
            stage = DiscoveryStage(stage)

        # Initial interview (no answer yet)
        if not user_message:

            interview = ask(
                memory=memory,
                stage=stage.value,
                latest_answer="",
            )

            return {
                "question": interview["question"],
                "completed": stage == DiscoveryStage.COMPLETE,
            }

        # Refine memory
        memory = refine(
            memory=memory,
            stage=stage.value,
            latest_answer=user_message,
        )

        # Ask interviewer what to do next
        interview = ask(
            memory=memory,
            stage=stage.value,
            latest_answer=user_message,
        )

        # Advance stage if AI decides
        if interview["next_stage"]:
            stage = self.STAGE_FLOW.get(
                stage,
                DiscoveryStage.COMPLETE,
            )

        # Persist project state
        project.discovery_memory = memory
        print("DISCOVERY MEMORY")
        print(memory)
        print("CONFIDENCE:", calculate_confidence(memory))
        project.discovery_stage = stage.value
        project.discovery_confidence = calculate_confidence(memory)

        return {
            "question": interview["question"],
            "completed": stage == DiscoveryStage.COMPLETE,
        }