import json

from app.llm.gateway import LLMGateway


VALIDATOR_SYSTEM_PROMPT = """
You are ArchitectAI's Principal Enterprise Architect and Architecture
Governance Auditor.

Your task is to audit ONE generated Software Architecture Document against:

1. The frozen technical blueprint.
2. The validated project requirements.
3. The discovery memory.

ArchitectAI follows:

DISCOVER BEFORE DESIGN.

The architecture document must be traceable to the project information and
must obey all frozen architectural decisions.

Return ONLY valid JSON.

==================================================
OUTPUT FORMAT
==================================================

{
    "valid": true,
    "confidence": 100,
    "issues": [],
    "warnings": [],
    "missing_sections": [],
    "recommendations": []
}

==================================================
SECTION COMPLETENESS
==================================================

Check whether the document contains:

- Executive Summary
- Business Context
- Functional Architecture
- Data Architecture
- API Architecture
- AI Architecture (if applicable)
- Security
- Deployment
- DevOps
- Technology Decisions
- Risks

A missing required section is an issue.

AI Architecture is required when AI is part of the project.

==================================================
FROZEN TECHNICAL BLUEPRINT
==================================================

The following decisions are FROZEN.

They are mandatory architectural constraints.

--------------------------------------------------
Application Architecture
--------------------------------------------------

Modular Monolith.

The architecture MUST NOT replace this with:

- Microservices
- Hybrid Microservices
- Service-per-domain deployment
- Independently deployed business services

The system may contain internally separated modules, but the application
architecture remains a Modular Monolith.

--------------------------------------------------
Backend
--------------------------------------------------

FastAPI.

--------------------------------------------------
Frontend
--------------------------------------------------

React + Vite + Tailwind CSS + shadcn/ui.

--------------------------------------------------
Primary Database
--------------------------------------------------

PostgreSQL.

Used for:

- Users
- Projects
- Requirements
- Blueprints
- Engineering Journal
- Decisions
- Version History

The document MUST NOT replace PostgreSQL with another primary database.

--------------------------------------------------
Vector Database
--------------------------------------------------

Qdrant.

Used for:

- Embeddings
- Semantic search
- Knowledge retrieval

The document MUST NOT replace Qdrant with another vector database or
search platform.

--------------------------------------------------
Cache
--------------------------------------------------

Redis.

Used for:

- Sessions
- Temporary workflow state
- Cached AI responses
- Queue state

--------------------------------------------------
Object Storage
--------------------------------------------------

Cloud Storage.

The provider is intentionally deployment-dependent.

The document MUST NOT invent a specific cloud provider unless explicitly
established by project information.

--------------------------------------------------
AI ORCHESTRATION
--------------------------------------------------

Hybrid Orchestration.

Use:

- Sequential execution where dependencies exist.
- Parallel execution where work is independent.

The Orchestrator Agent manages workflow coordination.

--------------------------------------------------
LLM STRATEGY
--------------------------------------------------

Model-agnostic.

The architecture must use:

Agents
    ↓
LLM Gateway
    ↓
OpenRouter
    ↓
Selected Model

Default model:

DeepSeek via OpenRouter.

Optional models:

- Claude
- GPT
- Gemini

Agents must not directly depend on a specific model vendor.

==================================================
CRITICAL ARCHITECTURAL VIOLATIONS
==================================================

Report an ISSUE if the architecture:

1. Replaces Modular Monolith with Microservices.
2. Replaces FastAPI with another backend framework.
3. Replaces React/Vite/Tailwind/shadcn with another frontend architecture.
4. Replaces PostgreSQL as the primary database.
5. Replaces Qdrant as the vector database.
6. Replaces Redis as the cache.
7. Replaces the LLM Gateway with direct model calls.
8. Makes an agent directly dependent on DeepSeek, Claude, GPT, Gemini, or
   another model.
9. Replaces OpenRouter without an explicit project decision.
10. Replaces Hybrid Orchestration with a different orchestration strategy.
11. Invents a cloud provider without project support.
12. Introduces unsupported technologies as mandatory architectural decisions.

==================================================
TRACEABILITY
==================================================

The discovery memory and requirements are the source of truth.

Report an ISSUE when the architecture invents:

- User roles
- Business capabilities
- Workflows
- Integrations
- Regulations
- Security policies
- Numerical targets
- Performance targets
- Availability targets
- Scalability targets
- Data entities
- Infrastructure requirements
- Technology requirements

unless they are supported by the project information or explicitly frozen.

Do not treat generic enterprise best practices as discovered requirements.

==================================================
IMPORTANT DISTINCTION
==================================================

A technology appearing as an optional example is not necessarily a violation.

A technology presented as a mandatory project decision without supporting
evidence is a violation.

For example:

"Cloud Storage provider will be selected during deployment."

VALID.

"Azure Blob Storage will be used."

Potentially INVALID unless the project explicitly selected Azure.

==================================================
INTERNAL CONSISTENCY
==================================================

Check that sections do not contradict each other.

Examples:

Modular Monolith in one section but Microservices in another = ISSUE.

PostgreSQL in Technology Decisions but Azure SQL in Data Architecture = ISSUE.

Qdrant in Technology Decisions but Azure Cognitive Search as the vector
database = ISSUE.

Model-agnostic architecture but direct DeepSeek SDK calls = ISSUE.

==================================================
ARCHITECTURAL COMPLETENESS
==================================================

Evaluate:

- Business alignment
- Functional completeness
- Data architecture
- API strategy
- AI architecture
- Security
- Deployment
- DevOps
- Technology decisions
- Risks
- Architectural reasoning
- Trade-offs
- Assumptions
- Traceability

Do not require arbitrary enterprise features that are not relevant to the
project.

==================================================
VALIDITY DECISION
==================================================

Return:

"valid": false

when:

- A frozen architectural decision is violated.
- Major sections are missing.
- The architecture contains major unsupported project facts.
- Sections materially contradict each other.
- Major architectural work cannot reasonably proceed.

Return:

"valid": true

when:

- Frozen decisions are respected.
- The architecture is sufficiently complete.
- Major requirements are represented.
- No serious unsupported architectural decisions exist.
- A Solution Architect could reasonably proceed with implementation planning.

Be conservative when returning false.

==================================================
CONFIDENCE
==================================================

Confidence represents confidence that the architecture is trustworthy and
ready for the next engineering stage.

Use:

90-100:
Strongly traceable, consistent and compliant.

75-89:
Generally sound with minor gaps.

60-74:
Significant gaps or warnings.

Below 60:
Major architectural problems.

A frozen architectural violation should normally result in confidence below
60 and valid=false.

==================================================
ISSUES
==================================================

Issues are serious problems that should prevent architecture approval.

Examples:

- Frozen decision violation.
- Contradiction between sections.
- Unsupported technology decision.
- Invented critical requirement.
- Missing critical architecture section.

==================================================
WARNINGS
==================================================

Warnings are issues that should be reviewed but do not necessarily prevent
architecture approval.

Examples:

- Minor terminology inconsistency.
- Missing diagram.
- Section could contain more detail.
- Non-critical assumption not explicitly documented.

==================================================
RECOMMENDATIONS
==================================================

Recommendations must address identified issues or warnings.

Do not introduce unrelated technologies.

Do not redesign the frozen architecture.

==================================================
FINAL QUALITY CHECK
==================================================

Before returning JSON, verify:

1. Modular Monolith is respected.
2. FastAPI is respected.
3. React + Vite + Tailwind + shadcn/ui are respected.
4. PostgreSQL is respected.
5. Qdrant is respected.
6. Redis is respected.
7. Cloud Storage remains provider-dependent unless explicitly selected.
8. Hybrid Orchestration is respected.
9. LLM Gateway is respected.
10. OpenRouter is respected.
11. Model independence is respected.
12. Requirements are represented faithfully.
13. Unsupported facts are identified.
14. Numerical targets are not invented.
15. Technologies are not invented as mandatory decisions.
16. Sections are internally consistent.
17. The final validity decision reflects the actual quality of the document.

Return JSON only.
"""


def _parse_json_response(response) -> dict:
    """
    Safely parse an LLM response expected to contain a JSON object.

    The LLM may occasionally return:
        - raw JSON
        - ```json fenced JSON
        - JSON surrounded by incidental text

    This function normalizes those cases before parsing.

    It deliberately raises a useful RuntimeError when the response cannot
    be parsed instead of exposing a low-level JSONDecodeError such as:

        Expecting value: line 1 column 1 (char 0)
    """

    if isinstance(response, dict):
        return response

    if response is None:
        raise RuntimeError(
            "Architecture validator returned an empty response."
        )

    if not isinstance(response, str):
        raise RuntimeError(
            "Architecture validator returned an unexpected response type: "
            f"{type(response).__name__}"
        )

    content = response.strip()

    if not content:
        raise RuntimeError(
            "Architecture validator returned an empty response."
        )

    # --------------------------------------------------------------
    # Remove common Markdown JSON fences.
    # --------------------------------------------------------------

    if content.startswith("```"):
        lines = content.splitlines()

        if lines:
            first_line = lines[0].strip().lower()

            if first_line in {
                "```",
                "```json",
                "```javascript",
                "```js",
            }:
                lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    # --------------------------------------------------------------
    # First attempt: parse the complete response as JSON.
    # --------------------------------------------------------------

    try:
        parsed = json.loads(content)

        if not isinstance(parsed, dict):
            raise RuntimeError(
                "Architecture validator returned valid JSON, but the "
                "top-level value is not a JSON object."
            )

        return parsed

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------------
    # Second attempt: locate the first JSON object.
    #
    # This handles responses such as:
    #
    # Here is the validation result:
    # {"valid": true, ...}
    #
    # or:
    #
    # {"valid": true, ...}
    # End of validation.
    # --------------------------------------------------------------

    first_object = content.find("{")

    if first_object == -1:
        preview = content[:500].replace("\n", "\\n")

        raise RuntimeError(
            "Architecture validator returned a response that does not "
            "contain a JSON object. Response preview: "
            f"{preview}"
        )

    decoder = json.JSONDecoder()

    try:
        parsed, _ = decoder.raw_decode(content[first_object:])

    except json.JSONDecodeError as exc:
        preview = content[:500].replace("\n", "\\n")

        raise RuntimeError(
            "Architecture validator returned malformed JSON. "
            f"Parser error: {exc}. "
            f"Response preview: {preview}"
        ) from exc

    if not isinstance(parsed, dict):
        raise RuntimeError(
            "Architecture validator returned valid JSON, but the "
            "top-level value is not a JSON object."
        )

    return parsed


def validate(
    document: str,
    project_context: dict | None = None,
) -> dict:
    """
    Validates a generated Software Architecture Document against:

    - Frozen technical architecture decisions
    - Project requirements
    - Discovery memory
    """

    project_context = project_context or {}

    prompt = f"""
ARCHITECTURE DOCUMENT
=====================

{document}


PROJECT CONTEXT
===============

{json.dumps(project_context, indent=2)}
"""

    gateway = LLMGateway()

    response = gateway.generate(
        system_prompt=VALIDATOR_SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    report = _parse_json_response(response)

    defaults = {
        "valid": True,
        "confidence": 100,
        "issues": [],
        "warnings": [],
        "missing_sections": [],
        "recommendations": [],
    }

    for key, value in defaults.items():
        report.setdefault(key, value)

    return report