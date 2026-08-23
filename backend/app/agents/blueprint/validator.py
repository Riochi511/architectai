from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Blueprint Overview",
    "Implementation Principles",
    "System Components",
    "Component Responsibilities",
    "Module Structure",
    "API Surface",
    "Data Layer",
    "AI and LLM Integration",
    "Orchestration Layer",
    "Security Boundaries",
    "Configuration and Environment",
    "Observability",
    "Error Handling",
    "Testing Strategy",
    "Deployment Boundaries",
    "Implementation Sequence",
    "Dependencies",
    "Engineering Constraints",
    "Blueprint Risks",
    "Assumptions",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Implementation Architect and
Blueprint Governance Auditor.

Your task is to audit a generated Implementation Blueprint against:

1. The frozen ArchitectAI architecture.
2. Discovery memory.
3. Validated requirements.
4. Approved architecture.
5. Approved technology decisions.
6. Approved database design.
7. Approved cost estimation.
8. Approved Critic report.

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

The Blueprint must not replace or contradict these decisions.

BLUEPRINT ROLE

The Blueprint translates approved engineering decisions into
implementation guidance.

It must not redesign:

- requirements;
- architecture;
- technology;
- database;
- cost strategy;
- orchestration strategy.

TRACEABILITY

Blueprint decisions must be supported by:

1. Discovery information.
2. Validated requirements.
3. Approved architecture.
4. Approved technology decisions.
5. Approved database design.
6. Approved cost estimation.
7. Critic findings.
8. Clearly identified assumptions.

PROJECT FACT DISCIPLINE

Report an ISSUE when the Blueprint invents unsupported:

- capabilities;
- user roles;
- integrations;
- APIs;
- database entities;
- infrastructure;
- performance targets;
- availability targets;
- traffic volumes;
- geographic regions;
- compliance requirements;
- business rules;
- deployment commitments.

FROZEN TECHNOLOGY COMPLIANCE

Report an ISSUE when:

- another primary database replaces PostgreSQL;
- another vector database replaces Qdrant;
- Redis is treated as the system of record;
- Cloud Storage is replaced by unsupported provider-specific
  infrastructure;
- direct model-provider dependencies bypass OpenRouter;
- model-specific logic violates model independence;
- Modular Monolith is replaced by Microservices;
- Hybrid Orchestration is contradicted.

IMPLEMENTATION DISCIPLINE

The Blueprint should describe implementation structure and
responsibilities without generating:

- source code;
- SQL;
- migrations;
- infrastructure-as-code;
- deployment scripts.

API DISCIPLINE

Report an ISSUE when unsupported API capabilities are presented
as confirmed requirements.

DATA DISCIPLINE

Report an ISSUE when unsupported entities or storage
responsibilities are introduced as confirmed architecture.

CROSS-STAGE CONSISTENCY

The Blueprint must remain consistent with:

Requirements
? Architecture
? Technology
? Database
? Cost
? Critic.

Report an ISSUE when the Blueprint introduces a contradiction
with any approved stage.

VALIDITY

Return valid=false when:

- a frozen architectural decision is violated;
- major approved decisions are contradicted;
- unsupported major capabilities are introduced;
- critical dependencies are omitted;
- the Blueprint is not implementation-safe;
- serious cross-stage contradictions exist.

Return valid=true when:

- approved architecture is preserved;
- implementation responsibilities are clear;
- dependencies are respected;
- major decisions are traceable;
- unsupported facts are not presented as confirmed;
- the Blueprint is suitable for implementation planning.

Do not mark invalid merely because:

- optional implementation details are unresolved;
- provider selection remains intentionally neutral;
- exact pricing is unavailable;
- minor implementation refinements remain.

CONFIDENCE

90-100:
Strongly traceable, consistent and implementation-ready.

75-89:
Generally sound with moderate non-blocking gaps.

60-74:
Significant implementation concerns.

Below 60:
Major Blueprint problems.

A frozen architectural violation should normally result in
confidence below 60 and valid=false.

Return JSON only.
"""


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Implementation Blueprint.

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
                "Generated blueprint document must be non-empty."
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

    for decision, token in frozen_expectations.items():
        if token not in document_lower:
            warnings.append(
                f"Frozen decision '{decision}' is not explicitly "
                f"mentioned in the Blueprint."
            )

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


APPROVED TECHNOLOGY
===================

{project_context.get(
    "technology",
    "",
)}


APPROVED DATABASE
=================

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


APPROVED CRITIC REPORT
======================

{project_context.get(
    "critic",
    "",
)}


BLUEPRINT
=========

{document}


Audit this Implementation Blueprint.

Check:

- requirements traceability;
- architecture consistency;
- technology consistency;
- database consistency;
- cost consistency;
- Critic consistency;
- frozen architecture compliance;
- module responsibility clarity;
- API discipline;
- data responsibility boundaries;
- AI and LLM abstraction;
- orchestration consistency;
- dependency ordering;
- unsupported capabilities;
- unsupported entities;
- unsupported integrations;
- unsupported infrastructure;
- invented project facts;
- implementation readiness;
- whether the Blueprint introduces architectural redesign.

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
                "Blueprint validator returned invalid JSON."
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
