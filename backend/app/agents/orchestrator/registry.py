from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from app.agents.orchestrator.context import (
    OrchestrationContext,
)
from app.agents.orchestrator.result import AgentResult


AgentCallable = Callable[
    [OrchestrationContext],
    AgentResult | dict[str, Any] | Awaitable[
        AgentResult | dict[str, Any]
    ],
]


@dataclass(frozen=True)
class AgentSpec:
    """
    Registration metadata for one workflow stage.
    """

    name: str
    handler: AgentCallable

    parallel_safe: bool = False
    required: bool = True


class AgentRegistry:
    """
    Central registry for ArchitectAI agents.

    The Orchestrator depends on this contract rather than concrete
    agent implementations.
    """

    def __init__(self) -> None:
        self._agents: dict[str, AgentSpec] = {}

    def register(
        self,
        name: str,
        handler: AgentCallable,
        *,
        parallel_safe: bool = False,
        required: bool = True,
    ) -> None:

        if name in self._agents:
            raise ValueError(
                f"Agent already registered: {name}"
            )

        self._agents[name] = AgentSpec(
            name=name,
            handler=handler,
            parallel_safe=parallel_safe,
            required=required,
        )

    def get(self, name: str) -> AgentSpec:
        try:
            return self._agents[name]
        except KeyError as exc:
            raise KeyError(
                f"No agent registered for stage: {name}"
            ) from exc

    def contains(self, name: str) -> bool:
        return name in self._agents

    def names(self) -> list[str]:
        return list(self._agents.keys())

    async def execute(
        self,
        name: str,
        context: OrchestrationContext,
    ) -> AgentResult:

        spec = self.get(name)

        result = spec.handler(context)

        if inspect.isawaitable(result):
            result = await result

        if isinstance(result, AgentResult):
            return result

        if isinstance(result, dict):
            return AgentResult.success(
                stage=name,
                output=result,
            )

        raise TypeError(
            f"Agent '{name}' returned unsupported type: "
            f"{type(result).__name__}"
        )