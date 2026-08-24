from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Workforce Overview",
    "Engineering Roles",
    "Responsibility Matrix",
    "Work Packages",
    "Implementation Tasks",
    "Task Dependencies",
    "Execution Order",
    "Required Skills",
    "Deliverables",
    "Coordination Model",
    "Workforce Assumptions",
    "Workforce Risks",
    "Workforce Readiness",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Engineering Workforce Architect
and Workforce Governance Auditor.

Your task is to audit a generated Engineering Workforce Plan
against:

1. The frozen ArchitectAI architecture.
2. Validated requirements.
3. Approved architecture.
4. Approved technology decisions.
5. Approved database design.
6. Approved cost estimation.
7. Approved Critic findings.
8. Approved Blueprint.

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

IMPORTANT OUTPUT RULES

- "issues" MUST be an array of strings.
- "warnings" MUST be an array of strings.
- "missing_sections" MUST be an array of section-name strings.
- "recommendations" MUST be an array of strings.
- Do not return objects/dictionaries inside these arrays.
- Do not return nested structures inside these arrays.
- If there are no items, return [].

WORKFORCE ROLE

The Workforce stage converts the approved Blueprint into an
executable engineering workforce plan.

It defines:

- responsibilities;
- engineering roles;
- work packages;
- implementation tasks;
- ownership;
- dependencies;
- execution order;
- required skills;
- deliverables;
- coordination boundaries;
- workforce assumptions;
- workforce risks.

It must not redesign the system.

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

These decisions must not be replaced by the Workforce plan.

TRACEABILITY

Workforce decisions must be supported by:

1. Blueprint.
2. Approved architecture.
3. Validated requirements.
4. Approved technology decisions.
5. Approved database design.
6. Approved cost estimation.
7. Approved Critic findings.
8. Clearly identified assumptions.

PROJECT FACT DISCIPLINE

Report an ISSUE when the Workforce plan invents unsupported:

- employee counts;
- staffing budgets;
- salaries;
- hiring timelines;
- organizational structures;
- team sizes;
- employee identities;
- contractor commitments;
- business roles;
- project timelines.

Do not treat assumptions as confirmed project facts.

TASK DISCIPLINE

Report an ISSUE when implementation tasks introduce
capabilities absent from the Blueprint or redesign approved
architecture.

DEPENDENCY DISCIPLINE

Report an ISSUE when:

- dependencies contradict the Blueprint;
- arbitrary dependencies are presented as required;
- required prerequisites are missing;
- execution order contradicts actual dependencies.

OWNERSHIP DISCIPLINE

Responsibilities must have clear ownership.

Ownership must describe engineering responsibility.

Do not invent employee identities.

DELIVERABLE DISCIPLINE

Major work packages should have concrete deliverables that
are traceable to the Blueprint.

INTERNAL CONSISTENCY

Report an ISSUE when:

- roles contradict responsibilities;
- tasks have impossible dependencies;
- ownership conflicts with work packages;
- deliverables are unrelated to the Blueprint;
- workforce assumptions contradict approved project information;
- frozen architecture is contradicted;
- model independence is violated.

VALIDITY

Return valid=false when:

- the Workforce plan contradicts frozen architecture;
- major Blueprint responsibilities are omitted;
- unsupported major project facts are presented as confirmed;
- critical implementation dependencies are missing;
- major responsibilities have no ownership;
- major work packages have no deliverables;
- serious internal contradictions exist;
- the Workforce plan is unsuitable for engineering execution planning.

Return valid=true when:

- the Workforce plan is traceable;
- responsibilities are clear;
- major Blueprint work is represented;
- ownership is defined;
- dependencies are coherent;
- deliverables are defined;
- unsupported facts are not presented as confirmed;
- no serious architectural contradictions exist.

Do not mark the plan invalid merely because:

- exact team size is unknown;
- hiring decisions are not made;
- exact timelines are unavailable;
- optional enterprise roles are absent.

CONFIDENCE

90-100:
Strongly traceable, complete and execution-ready.

75-89:
Generally sound with moderate non-blocking gaps.

60-74:
Significant workforce planning uncertainty.

Below 60:
Major workforce planning problems.

A frozen architectural violation should normally result in
confidence below 60 and valid=false.

Return JSON only.
"""


def _normalize_string_list(
    value,
    field_name: str,
) -> list[str]:
    """
    Normalize validator output fields that are expected to
    contain strings.

    The LLM is instructed to return string arrays, but model
    output must never be trusted blindly. This prevents
    dictionaries/lists from leaking into downstream operations
    such as dict.fromkeys().
    """

    if not isinstance(value, list):
        return [
            f"Validator returned an invalid {field_name} structure."
        ]

    normalized: list[str] = []

    for item in value:
        if isinstance(item, str):
            text = item.strip()

            if text:
                normalized.append(text)

        elif isinstance(item, dict):
            # Preserve useful information without allowing the
            # dictionary itself to become an unhashable value.
            try:
                normalized.append(
                    json.dumps(
                        item,
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                )
            except (TypeError, ValueError):
                normalized.append(
                    f"Validator returned a dictionary in {field_name}."
                )

        elif item is not None:
            normalized.append(str(item))

    return normalized


def _deduplicate_strings(
    values: list[str],
) -> list[str]:
    """
    Deduplicate string values while preserving their original
    order.
    """

    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        if not isinstance(value, str):
            continue

        normalized = value.strip()

        if not normalized:
            continue

        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Engineering Workforce Plan.

    Validation has two layers:

    1. Deterministic structural validation.
    2. LLM semantic workforce governance validation.
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
                "Generated workforce document must be non-empty."
            ],
            "warnings": [],
            "missing_sections": sorted(
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
                f"mentioned in the Workforce plan."
            )

    prompt = f"""
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


APPROVED CRITIC FINDINGS
========================

{project_context.get(
    "critic",
    "",
)}


APPROVED BLUEPRINT
==================

{project_context.get(
    "blueprint",
    "",
)}


DISCOVERY MEMORY
================

{json.dumps(
    project_context.get(
        "discovery_memory",
        {},
    ),
    indent=2,
)}


WORKFORCE PLAN
==============

{document}


Audit this Engineering Workforce Plan.

Check:

- Blueprint traceability;
- requirements traceability;
- architecture consistency;
- technology consistency;
- database consistency;
- cost consistency;
- Critic finding coverage;
- responsibility completeness;
- task completeness;
- ownership clarity;
- dependency correctness;
- execution order;
- deliverable traceability;
- unsupported workforce assumptions;
- invented staffing facts;
- invented timelines;
- frozen architecture compliance;
- model independence;
- suitability for actual engineering execution planning.

Do not invent issues.

Do not redesign the system.

Return the validation report.

REMINDER:

The following fields MUST contain only strings:

"issues"
"warnings"
"missing_sections"
"recommendations"

Do not place dictionaries or nested objects inside those arrays.
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
                "Workforce validator returned invalid JSON."
            ],
            "warnings": [],
            "missing_sections": [],
            "recommendations": [],
        }

    if not isinstance(report, dict):
        report = {
            "valid": False,
            "confidence": 0,
            "issues": [
                "Workforce validator returned an invalid report structure."
            ],
            "warnings": [],
            "missing_sections": [],
            "recommendations": [],
        }

    # --------------------------------------------------
    # Normalize LLM Output
    # --------------------------------------------------
    #
    # Never trust the LLM to return exactly the structure
    # requested by the system prompt.
    #
    # In particular, missing_sections previously contained
    # dictionaries, which caused:
    #
    #     TypeError: unhashable type: 'dict'
    #
    # when dict.fromkeys() was called.
    # --------------------------------------------------

    report_issues = _normalize_string_list(
        report.get(
            "issues",
            [],
        ),
        "issues",
    )

    report_warnings = _normalize_string_list(
        report.get(
            "warnings",
            [],
        ),
        "warnings",
    )

    report_missing_sections = _normalize_string_list(
        report.get(
            "missing_sections",
            [],
        ),
        "missing_sections",
    )

    recommendations = _normalize_string_list(
        report.get(
            "recommendations",
            [],
        ),
        "recommendations",
    )

    # --------------------------------------------------
    # Merge Deterministic + LLM Validation
    # --------------------------------------------------

    issues.extend(report_issues)
    warnings.extend(report_warnings)

    combined_missing_sections = _deduplicate_strings(
        missing_sections
        + report_missing_sections
    )

    # --------------------------------------------------
    # Final Validation State
    # --------------------------------------------------

    valid = (
        len(issues) == 0
        and len(combined_missing_sections) == 0
    )

    # --------------------------------------------------
    # Normalize Confidence
    # --------------------------------------------------

    confidence = report.get(
        "confidence",
        100,
    )

    try:
        confidence = int(confidence)
    except (TypeError, ValueError):
        confidence = 0

    confidence = max(
        0,
        min(
            confidence,
            100,
        ),
    )

    # --------------------------------------------------
    # Return Final Validation Report
    # --------------------------------------------------

    return {
        "valid": valid,
        "confidence": confidence,
        "issues": _deduplicate_strings(
            issues
        ),
        "warnings": _deduplicate_strings(
            warnings
        ),
        "missing_sections": combined_missing_sections,
        "recommendations": _deduplicate_strings(
            recommendations
        ),
    }