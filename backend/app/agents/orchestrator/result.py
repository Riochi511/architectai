from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AgentResult:
    """
    Standard result returned by every orchestrated agent.
    """

    stage: str
    status: AgentStatus
    output: dict[str, Any] | None = None

    error: str | None = None

    duration_ms: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def succeeded(self) -> bool:
        return self.status == AgentStatus.SUCCESS

    @property
    def failed(self) -> bool:
        return self.status == AgentStatus.FAILED

    @property
    def skipped(self) -> bool:
        return self.status == AgentStatus.SKIPPED

    @classmethod
    def success(
        cls,
        stage: str,
        output: dict[str, Any] | None = None,
        duration_ms: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> "AgentResult":

        return cls(
            stage=stage,
            status=AgentStatus.SUCCESS,
            output=output or {},
            duration_ms=duration_ms,
            metadata=metadata or {},
        )

    @classmethod
    def failure(
        cls,
        stage: str,
        error: str,
        duration_ms: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> "AgentResult":

        return cls(
            stage=stage,
            status=AgentStatus.FAILED,
            error=error,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )

    @classmethod
    def skipped(
        cls,
        stage: str,
        reason: str,
    ) -> "AgentResult":

        return cls(
            stage=stage,
            status=AgentStatus.SKIPPED,
            error=reason,
        )