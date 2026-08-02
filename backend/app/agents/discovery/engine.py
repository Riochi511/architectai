from app.agents.discovery.memory import DiscoveryMemory
from app.agents.discovery.questions import DISCOVERY_QUESTIONS
from app.agents.discovery.confidence import calculate_confidence
from app.agents.discovery.schemas import DiscoveryStage


class DiscoveryEngine:

    def __init__(self):
        self.memory = DiscoveryMemory()

    def process(self, answer: str | None = None):

        if answer:

            stage = self.memory.current_stage

            if stage == DiscoveryStage.VISION:
                self.memory.vision = answer
                self.memory.current_stage = DiscoveryStage.USERS

            elif stage == DiscoveryStage.USERS:
                self.memory.primary_users = answer
                self.memory.current_stage = DiscoveryStage.PROBLEM

            elif stage == DiscoveryStage.PROBLEM:
                self.memory.problem_statement = answer
                self.memory.current_stage = DiscoveryStage.FUNCTIONAL

            elif stage == DiscoveryStage.FUNCTIONAL:
                self.memory.functional_requirements.append(answer)
                self.memory.current_stage = DiscoveryStage.NON_FUNCTIONAL

            elif stage == DiscoveryStage.NON_FUNCTIONAL:
                self.memory.non_functional_requirements.append(answer)
                self.memory.current_stage = DiscoveryStage.AI

            elif stage == DiscoveryStage.AI:
                self.memory.ai_capabilities.append(answer)
                self.memory.current_stage = DiscoveryStage.DATA

            elif stage == DiscoveryStage.DATA:
                self.memory.data_sources.append(answer)
                self.memory.current_stage = DiscoveryStage.CONSTRAINTS

            elif stage == DiscoveryStage.CONSTRAINTS:
                self.memory.constraints.append(answer)
                self.memory.current_stage = DiscoveryStage.DEPLOYMENT

            elif stage == DiscoveryStage.DEPLOYMENT:
                self.memory.deployment_target = answer

        self.memory.confidence_score = calculate_confidence(self.memory)

        questions = DISCOVERY_QUESTIONS.get(
            self.memory.current_stage,
            [],
        )

        if questions:
            return {
                "question": questions[0],
                "completed": False,
            }

        return {
            "question": None,
            "completed": True,
        }