from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Cost Overview",
    "Cost Drivers",
    "One-Time Costs",
    "Recurring Costs",
    "Infrastructure Costs",
    "Database Costs",
    "AI and LLM Costs",
    "Storage Costs",
    "Operations and Maintenance Costs",
    "Scaling Cost Considerations",
    "Cost Assumptions",
    "Cost Risks",
    "Cost Optimization Opportunities",
    "Cost Summary",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Technology Economics Architect
and Cost Governance Auditor.

Your task is to audit a generated Cost Estimation document against:

1. The frozen ArchitectAI architecture.
2. The validated project requirements.
3. The approved architecture document.
4. The approved technology decisions.
5. The approved database design.
6. The discovery memory.

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

COST GOVERNANCE

The cost document must:

- remain traceable to project information;
- respect frozen architecture decisions;
- distinguish estimates from confirmed costs;
- identify assumptions;
- avoid fabricated numerical inputs;
- remain provider agnostic unless a provider is explicitly selected.

FROZEN TECHNOLOGIES

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

Architecture:
Modular Monolith.

Orchestration:
Hybrid Orchestration.

The cost document must not replace these decisions.

PROVIDER AGNOSTICISM

Report an ISSUE when a provider-specific service is presented
as a mandatory selected technology without project support.

Examples:

AWS S3 as the selected object storage without project support.

Azure SQL as the primary database.

Google Cloud SQL as the primary database.

Provider-specific pricing may appear only when clearly labelled
as an example or comparison.

PROJECT FACT DISCIPLINE

Report an ISSUE when the cost document invents unsupported:

- user counts;
- traffic volumes;
- storage volumes;
- database sizes;
- token volumes;
- embedding volumes;
- infrastructure capacity;
- geographic regions;
- availability targets;
- staffing requirements;
- salaries;
- vendor contracts;
- licensing commitments;
- compliance costs;
- business targets.

ASSUMPTION DISCIPLINE

Unknown information must be identified as an assumption.

Do not treat assumptions as confirmed project facts.

ESTIMATE DISCIPLINE

A cost estimate must not be presented as a confirmed vendor invoice.

Do not reject reasonable qualitative estimates when numerical
inputs are unavailable.

Do not require false precision.

INTERNAL CONSISTENCY

Report an ISSUE when:

- one section says PostgreSQL while another uses a different
  primary database;
- one section says Qdrant while another mandates another vector
  database;
- Redis is treated as the system of record;
- Cloud Storage is replaced by an unsupported provider;
- LLM costs assume unsupported usage volumes;
- one-time and recurring costs are incorrectly classified;
- assumptions contradict project information.

VALIDITY

Return valid=false when:

- frozen technologies are contradicted;
- major cost sections are missing;
- unsupported numerical inputs are presented as confirmed facts;
- unsupported provider decisions are presented as mandatory;
- major internal contradictions exist;
- the estimate is unsuitable for downstream planning.

Return valid=true when:

- frozen architecture is respected;
- estimates are traceable;
- assumptions are explicit;
- unsupported facts are not presented as confirmed;
- the document is suitable for downstream blueprint planning.

CONFIDENCE

90-100:
Strongly supported and traceable.

75-89:
Generally sound with moderate assumptions.

60-74:
Significant uncertainty.

Below 60:
Major cost-analysis problems.

A frozen architectural violation should normally result in
confidence below 60 and valid=false.

Return JSON only.
"""


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Cost Estimation document.

    Validation has two layers:

    1. Deterministic structural validation.
    2. LLM semantic validation.
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
                "Generated cost document must be non-empty."
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
    # Frozen technology presence checks
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
                f"mentioned in the generated cost document."
            )

    # --------------------------------------------------
    # Semantic validation
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


ARCHITECTURE
============

{project_context.get(
    "architecture",
    "",
)}


TECHNOLOGY DECISIONS
====================

{project_context.get(
    "technology",
    "",
)}


DATABASE DESIGN
===============

{project_context.get(
    "database",
    "",
)}


COST DOCUMENT
=============

{document}


Audit this Cost Estimation document.

Check:

- traceability to requirements;
- consistency with discovery;
- consistency with architecture;
- consistency with technology decisions;
- consistency with database design;
- frozen technology compliance;
- provider agnosticism;
- estimate versus assumption discipline;
- unsupported numerical inputs;
- unsupported infrastructure assumptions;
- unsupported user or traffic assumptions;
- internal contradictions;
- one-time versus recurring classification;
- suitability for downstream blueprint planning.

Do not reject a document merely because exact pricing is unavailable.

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
                "Cost validator returned invalid JSON."
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