from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Critique Overview",
    "Requirements Traceability",
    "Architecture Consistency",
    "Technology Consistency",
    "Database Consistency",
    "Cost Consistency",
    "Cross-Stage Contradictions",
    "Unsupported Decisions",
    "Architectural Risks",
    "Engineering Gaps",
    "Blueprint Readiness",
    "Critical Findings",
    "Recommendations",
    "Assumptions",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Architecture Governance Critic
and Governance Auditor.

Your task is to audit a generated Architecture and Engineering
Critique against:

1. The frozen ArchitectAI architecture.
2. Discovery memory.
3. Validated requirements.
4. Approved architecture.
5. Approved technology decisions.
6. Approved database design.
7. Approved cost estimation.

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

Architecture:
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

Orchestration:
Hybrid Orchestration.

The Critic must not recommend replacing these decisions.

GOVERNANCE ROLE

The Critic is a cross-stage governance layer.

It must evaluate whether the accumulated engineering artifacts
are internally consistent and ready for Blueprint generation.

It must not redesign the architecture.

TRACEABILITY

The critique must be supported by:

1. Discovery information.
2. Validated requirements.
3. Approved architecture.
4. Approved technology decisions.
5. Approved database design.
6. Approved cost estimation.
7. Frozen architecture decisions.
8. Clearly identified assumptions.

PROJECT FACT DISCIPLINE

Report an ISSUE when the critique incorrectly treats unsupported
information as confirmed project information.

Also report an ISSUE when the Critic misses a major unsupported
decision that materially affects Blueprint generation.

CROSS-STAGE CONSISTENCY

Report an ISSUE when major artifacts contradict one another.

Examples:

- Requirements describe a capability absent from Architecture.
- Architecture selects technology contradicting Technology Decisions.
- Technology selects a database contradicting Database Design.
- Database introduces unsupported primary data systems.
- Cost depends on unsupported architecture or usage assumptions.
- OpenRouter is selected but direct model-provider dependencies
  are accepted.
- Modular Monolith is contradicted by another stage.

SEVERITY DISCIPLINE

Critical:
Prevents safe Blueprint generation.

High:
Major issue requiring resolution before Blueprint generation.

Medium:
Meaningful issue that should be addressed.

Low:
Minor quality issue.

Informational:
Observation without a defect.

VALIDITY

Return valid=false when:

- a frozen architectural decision is violated;
- a major cross-stage contradiction exists;
- critical unsupported project facts exist;
- critical requirements are not traceable;
- the critique incorrectly approves a materially unsafe package;
- major Blueprint blockers are identified.

Return valid=true when:

- the engineering package is internally consistent;
- frozen architecture is respected;
- major requirements are traceable;
- technology and database decisions align;
- cost reasoning aligns with architecture;
- no critical Blueprint blockers exist.

Do not mark the package invalid merely because:

- exact cloud pricing is unavailable;
- provider selection is intentionally deferred;
- optional enterprise practices are not documented;
- minor non-blocking improvements remain.

CONFIDENCE

90-100:
Strongly traceable, consistent and Blueprint-ready.

75-89:
Generally sound with moderate non-blocking gaps.

60-74:
Significant unresolved concerns.

Below 60:
Major governance problems or Blueprint blockers.

A frozen architectural violation should normally result in
confidence below 60 and valid=false.

Return JSON only.
"""


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated cross-stage Critic report.

    Validation has two layers:

    1. Deterministic structural validation.
    2. LLM semantic governance validation.
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
                "Generated critic document must be non-empty."
            ],
            "warnings": [],
            "missing_sections": list(
                REQUIRED_SECTIONS
            ),
            "recommendations": [],
        }

    document_lower = document.lower()

    for section in REQUIRED_SECTIONS:
        if section.lower() not in document_lower:
            missing_sections.append(section)

    # --------------------------------------------------
    # Frozen architecture presence checks
    # --------------------------------------------------

    frozen_expectations = {
        "Modular Monolith": "modular monolith",
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
        "Hybrid Orchestration": "hybrid orchestration",
    }

    for architecture_decision, token in frozen_expectations.items():
        if token not in document_lower:
            warnings.append(
                f"Frozen decision '{architecture_decision}' is not "
                f"explicitly mentioned in the Critic report."
            )

    # --------------------------------------------------
    # Semantic governance validation
    # --------------------------------------------------

    prompt = f"""
DISCOVERY MEMORY
================

{json.dumps(
    project_context.get(
        "discovery_memory",
        {},
    ),
    indent=2,
)}


VALIDATED REQUIREMENTS
======================

{json.dumps(
    project_context.get(
        "requirements",
        {},
    ),
    indent=2,
)}


APPROVED ARCHITECTURE
=====================

{project_context.get(
    "architecture",
    "",
)}


APPROVED TECHNOLOGY DECISIONS
=============================

{project_context.get(
    "technology",
    "",
)}


APPROVED DATABASE DESIGN
========================

{project_context.get(
    "database",
    "",
)}


APPROVED COST ESTIMATION
========================

{project_context.get(
    "cost",
    "",
)}


CRITIC REPORT
=============

{document}


Audit this Critic report.

Check:

- requirements traceability;
- architecture consistency;
- technology consistency;
- database consistency;
- cost consistency;
- cross-stage contradictions;
- frozen architecture compliance;
- unsupported project facts;
- unsupported numerical assumptions;
- model independence;
- OpenRouter abstraction;
- provider agnosticism;
- Blueprint readiness;
- whether the Critic itself has made unsupported recommendations;
- whether the Critic incorrectly approves a serious architectural
  contradiction.

Do not invent issues.

Do not redesign the architecture.

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
                "Critic validator returned invalid JSON."
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
