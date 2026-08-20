class OrchestrationError(Exception):
    """Base exception for ArchitectAI orchestration errors."""


class AgentNotRegisteredError(OrchestrationError):
    """Raised when a workflow stage has no registered agent."""


class WorkflowDefinitionError(OrchestrationError):
    """Raised when the workflow graph is invalid."""


class StageExecutionError(OrchestrationError):
    """Raised when an agent fails during execution."""


class GateFailedError(OrchestrationError):
    """Raised when a quality gate prevents workflow progression."""