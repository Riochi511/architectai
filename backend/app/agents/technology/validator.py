from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Technology Overview",
    "Technology Stack",
    "Decision Criteria",
    "Technology Decisions",
    "Alternatives Considered",
    "Trade-offs",
    "Risks",
    "Assumptions",
}


FROZEN_TECHNOLOGIES = {
    "FastAPI",
    "React",
    "Vite",
    "Tailwind CSS",
    "shadcn/ui",
    "PostgreSQL",
    "Qdrant",
    "Redis",
    "Cloud Storage",
    "OpenRouter",
    "DeepSeek",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Technology Architect and
Technology Governance Auditor.

Your task is to audit a generated Technology Decisions document
against:

1. The frozen ArchitectAI architecture.
2. The validated project requirements.
3. The completed architecture document.
4. The discovery memory.

The technology document must remain traceable to project information
and must not contradict frozen architectural decisions.

Return ONLY valid JSON.

OUTPUT FORMAT

{
    "valid": true,
    "confidence": 100,
    "issues": [],
    "warnings": [],
    "missing_sections": [],
    "recommendations": []
}

FROZEN ARCHITECTURE

Architecture Style:
Modular Monolith.

Backend:
FastAPI.

Frontend:
React + Vite + Tailwind CSS + shadcn/ui.

Primary Database:
PostgreSQL.

Vector Database:
Qdrant.

Cache:
Redis.

Object Storage:
Cloud Storage.

LLM Gateway:
OpenRouter.

Default LLM:
DeepSeek via OpenRouter.

AI Architecture:
Model-agnostic.

AI Coordination:
Hybrid Orchestration.

The technology document MUST NOT replace or contradict these
decisions.

MODEL INDEPENDENCE

DeepSeek is the default model through OpenRouter.

The architecture must remain model-agnostic.

Direct dependencies on a specific model provider are architectural
violations.

PROVIDER AGNOSTICISM

Do not require a specific cloud provider unless the project
context explicitly specifies one.

Do not invent:

- AWS
- Azure
- Google Cloud
- Amazon S3
- Azure Blob Storage
- Google Cloud Storage
- Amazon RDS
- Azure SQL
- Google Cloud SQL

as mandatory decisions without project support.

TRACEABILITY

Technology decisions must be supported by:

1. Frozen architecture decisions.
2. Explicit project requirements.
3. Discovery information.
4. Clearly identified assumptions.

Do not treat common enterprise technology choices as project facts.

PROJECT FACT DISCIPLINE

Do not invent:

- user counts
- performance targets
- availability targets
- costs
- geographic regions
- regulatory obligations
- timelines
- infrastructure capacity
- integrations
- business targets

unless supported by the supplied project context.

INTERNAL CONSISTENCY

Report an ISSUE when the document contradicts itself.

Examples:

Modular Monolith in one section but Microservices in another.

PostgreSQL in one section but another primary database elsewhere.

Qdrant described as the vector database in one section but another
vector platform is presented as the mandatory choice.

OpenRouter is specified but agents directly call an LLM provider.

Model-agnostic architecture but a specific model is hard-coded into
application logic.

ALTERNATIVES

Alternatives may be discussed for comparison.

They must not silently replace frozen technologies.

VALIDITY

Return valid=false when:

- a frozen technology is replaced;
- the architecture is materially contradicted;
- major required technology decisions are missing;
- unsupported technologies are presented as mandatory;
- major project facts are invented;
- serious internal contradictions exist.

Return valid=true when:

- frozen technologies are respected;
- technology decisions are traceable;
- major technology decisions are sufficiently complete;
- no serious unsupported decisions exist;
- the document is suitable for downstream cost and blueprint planning.

CONFIDENCE

Use:

90-100:
Strongly traceable, consistent and compliant.

75-89:
Generally sound with minor gaps.

60-74:
Significant gaps or warnings.

Below 60:
Major technology problems.

A frozen technology violation should normally result in
confidence below 60 and valid=false.

ISSUES

Issues are serious problems that should prevent Technology approval.

WARNINGS

Warnings are quality concerns that should be reviewed but do not
necessarily prevent approval.

RECOMMENDATIONS

Recommendations must address identified issues or warnings.

Do not redesign the frozen architecture.

Return JSON only.
"""


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Technology Decisions document.

    Validation has two layers:

    1. Deterministic structural validation.
    2. LLM semantic validation.

    The final validity decision combines both layers.
    """

    project_context = project_context or {}

    issues: list[str] = []
    warnings: list[str] = []
    missing_sections: list[str] = []

    if not isinstance(document, str) or not document.strip():
        return {
            "valid": False,
            "confidence": 0,
            "issues": [
                "Generated technology document must be non-empty."
            ],
            "warnings": [],
            "missing_sections": list(
                REQUIRED_SECTIONS
            ),
            "recommendations": [],
        }

    # --------------------------------------------------
    # Structural validation
    # --------------------------------------------------

    document_lower = document.lower()

    for section in REQUIRED_SECTIONS:
        if section.lower() not in document_lower:
            missing_sections.append(section)

    # --------------------------------------------------
    # Frozen technology checks
    # --------------------------------------------------

    frozen_expectations = {
        "FastAPI": "fastapi",
        "React": "react",
        "Vite": "vite",
        "Tailwind CSS": "tailwind",
        "shadcn/ui": "shadcn",
        "PostgreSQL": "postgresql",
        "Qdrant": "qdrant",
        "Redis": "redis",
        "Cloud Storage": "cloud storage",
        "OpenRouter": "openrouter",
        "DeepSeek": "deepseek",
    }

    for technology, token in frozen_expectations.items():
        if token not in document_lower:
            warnings.append(
                f"Frozen technology '{technology}' is not explicitly "
                f"mentioned in the generated document."
            )

    # --------------------------------------------------
    # LLM semantic validation
    # --------------------------------------------------

    prompt = f"""
DISCOVERY MEMORY
================

{json.dumps(
    project_context.get("discovery_memory", {}),
    indent=2,
)}


VALIDATED REQUIREMENTS
======================

{json.dumps(
    project_context.get("requirements", {}),
    indent=2,
)}


ARCHITECTURE
============

{project_context.get(
    "architecture",
    "",
)}


TECHNOLOGY DOCUMENT
===================

{document}


Audit this Technology Decisions document.

Check:

- traceability to requirements;
- consistency with discovery;
- consistency with architecture;
- compliance with frozen technologies;
- model independence;
- OpenRouter abstraction;
- provider agnosticism;
- unsupported technologies;
- invented project facts;
- invented numerical targets;
- internal contradictions;
- completeness of technology decisions;
- whether the document is suitable for downstream cost estimation;
- whether the document is suitable for blueprint generation.

Do not reject a document merely because an optional implementation
detail is absent.

Do not invent issues.

Return the validation report.
"""

    gateway = LLMGateway()

    content = gateway.generate(
        system_prompt=VALIDATOR_SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    try:
        report = json.loads(content)
    except (TypeError, json.JSONDecodeError):
        report = {
            "valid": False,
            "confidence": 0,
            "issues": [
                "Technology validator returned invalid JSON."
            ],
            "warnings": [],
            "missing_sections": [],
            "recommendations": [],
        }

    if not isinstance(report, dict):
        report = {}

    report_issues = report.get(
        "issues",
        [],
    )

    report_warnings = report.get(
        "warnings",
        [],
    )

    report_missing_sections = report.get(
        "missing_sections",
        [],
    )

    recommendations = report.get(
        "recommendations",
        [],
    )

    if not isinstance(report_issues, list):
        report_issues = [
            "Validator returned an invalid issues structure."
        ]

    if not isinstance(report_warnings, list):
        report_warnings = [
            "Validator returned an invalid warnings structure."
        ]

    if not isinstance(report_missing_sections, list):
        report_missing_sections = []

    if not isinstance(recommendations, list):
        recommendations = []

    issues.extend(report_issues)
    warnings.extend(report_warnings)

    combined_missing_sections = list(
        dict.fromkeys(
            missing_sections
            + report_missing_sections
        )
    )

    valid = (
        len(issues) == 0
        and len(combined_missing_sections) == 0
    )

    return {
        "valid": valid,
        "confidence": report.get(
            "confidence",
            100,
        ),
        "issues": issues,
        "warnings": warnings,
        "missing_sections": combined_missing_sections,
        "recommendations": recommendations,
    }