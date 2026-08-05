from dataclasses import dataclass

from app.agents.architecture.prompts import (
    EXECUTIVE_SUMMARY_PROMPT,
    BUSINESS_CONTEXT_PROMPT,
    FUNCTIONAL_ARCHITECTURE_PROMPT,
    DATA_ARCHITECTURE_PROMPT,
    API_ARCHITECTURE_PROMPT,
    AI_ARCHITECTURE_PROMPT,
    SECURITY_PROMPT,
    DEPLOYMENT_PROMPT,
    DEVOPS_PROMPT,
    TECHNOLOGY_DECISIONS_PROMPT,
    RISKS_PROMPT,
)


@dataclass(frozen=True)
class ArchitectureSection:
    """
    Represents one section of the Software
    Architecture Document.
    """

    id: str
    title: str
    prompt: str


SECTION_REGISTRY = [

    ArchitectureSection(
        id="executive_summary",
        title="Executive Summary",
        prompt=EXECUTIVE_SUMMARY_PROMPT,
    ),

    ArchitectureSection(
        id="business_context",
        title="Business Context",
        prompt=BUSINESS_CONTEXT_PROMPT,
    ),

    ArchitectureSection(
        id="functional_architecture",
        title="Functional Architecture",
        prompt=FUNCTIONAL_ARCHITECTURE_PROMPT,
    ),

    ArchitectureSection(
        id="data_architecture",
        title="Data Architecture",
        prompt=DATA_ARCHITECTURE_PROMPT,
    ),

    ArchitectureSection(
        id="api_architecture",
        title="API Architecture",
        prompt=API_ARCHITECTURE_PROMPT,
    ),

    ArchitectureSection(
        id="ai_architecture",
        title="AI Architecture",
        prompt=AI_ARCHITECTURE_PROMPT,
    ),

    ArchitectureSection(
        id="security",
        title="Security",
        prompt=SECURITY_PROMPT,
    ),

    ArchitectureSection(
        id="deployment",
        title="Deployment",
        prompt=DEPLOYMENT_PROMPT,
    ),

    ArchitectureSection(
        id="devops",
        title="DevOps",
        prompt=DEVOPS_PROMPT,
    ),

    ArchitectureSection(
        id="technology_decisions",
        title="Technology Decisions",
        prompt=TECHNOLOGY_DECISIONS_PROMPT,
    ),

    ArchitectureSection(
        id="risks",
        title="Risks",
        prompt=RISKS_PROMPT,
    ),
]