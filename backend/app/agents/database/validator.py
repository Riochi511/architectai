from __future__ import annotations

import json

from app.llm.gateway import LLMGateway


REQUIRED_SECTIONS = {
    "Data Architecture Overview",
    "Data Domains",
    "Core Entities",
    "Entity Relationships",
    "Persistence Strategy",
    "PostgreSQL Design",
    "Vector Data Strategy",
    "Cache Data Strategy",
    "Object Storage Strategy",
    "Indexing Strategy",
    "Transaction and Consistency Strategy",
    "Data Lifecycle",
    "Data Security",
    "Backup and Recovery",
    "Trade-offs",
    "Risks",
    "Assumptions",
}


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Database Architect and
Database Governance Auditor.

Your task is to audit a generated Database Design document against:

1. The frozen ArchitectAI architecture.
2. The validated project requirements.
3. The approved architecture document.
4. The approved technology decisions.
5. The discovery memory.

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

FROZEN DATA ARCHITECTURE

Primary Database:
PostgreSQL.

Vector Database:
Qdrant.

Cache:
Redis.

Object Storage:
Cloud Storage.

These technologies must not be replaced or contradicted.

DATA RESPONSIBILITIES

PostgreSQL:
Durable relational application data.

Qdrant:
Embeddings and semantic retrieval data where required.

Redis:
Cache and temporary/short-lived state where applicable.

Cloud Storage:
Object/blob-oriented data where required.

SQL

The document must not contain executable SQL as part of the
database architecture deliverable.

TRACEABILITY

Database decisions must be supported by:

1. Frozen architecture.
2. Validated requirements.
3. Discovery information.
4. Approved architecture.
5. Approved technology decisions.
6. Clearly identified assumptions.

Do not treat common enterprise database practices as confirmed
project facts.

PROJECT FACT DISCIPLINE

Report an ISSUE when the document invents unsupported:

- entities
- integrations
- data volumes
- retention requirements
- compliance requirements
- performance targets
- availability targets
- RPO values
- RTO values
- infrastructure capacity
- business rules

INTERNAL CONSISTENCY

Report an ISSUE when storage responsibilities contradict each other.

Examples:

PostgreSQL is the primary database in one section but another
relational database is presented as the primary system elsewhere.

Qdrant is identified as the vector database but another vector
platform is made mandatory.

Redis is treated as the system of record.

Cloud Storage is replaced by a specific cloud provider without
project support.

VALIDITY

Return valid=false when:

- a frozen storage technology is replaced;
- major database sections are missing;
- unsupported entities are presented as confirmed facts;
- major storage responsibilities contradict the architecture;
- serious internal contradictions exist;
- the design is unsuitable for downstream cost or blueprint planning.

Return valid=true when:

- frozen storage technologies are respected;
- database responsibilities are clear;
- major data decisions are traceable;
- unsupported facts are not presented as confirmed;
- the design is suitable for downstream planning.

CONFIDENCE

90-100:
Strongly traceable, consistent and complete.

75-89:
Generally sound with minor gaps.

60-74:
Significant gaps or warnings.

Below 60:
Major database problems.

A frozen technology violation should normally result in
confidence below 60 and valid=false.

Return JSON only.
"""


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Database Design document.

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
                "Generated database document must be non-empty."
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
        "PostgreSQL": "postgresql",
        "Qdrant": "qdrant",
        "Redis": "redis",
        "Cloud Storage": "cloud storage",
    }

    for technology, token in frozen_expectations.items():
        if token not in document_lower:
            warnings.append(
                f"Frozen technology '{technology}' is not explicitly "
                f"mentioned in the generated document."
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


DATABASE DOCUMENT
=================

{document}


Audit this Database Design document.

Check:

- traceability to requirements;
- consistency with discovery;
- consistency with architecture;
- consistency with technology decisions;
- PostgreSQL compliance;
- Qdrant compliance;
- Redis compliance;
- Cloud Storage provider neutrality;
- unsupported entities;
- unsupported integrations;
- invented numerical targets;
- unsupported retention or compliance requirements;
- internal contradictions;
- completeness;
- suitability for downstream cost planning;
- suitability for blueprint generation.

Do not reject a document merely because optional implementation
details are absent.

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
                "Database validator returned invalid JSON."
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