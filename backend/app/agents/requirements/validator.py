import json

from app.llm.gateway import LLMGateway
from app.agents.requirements.prompts import VALIDATOR_PROMPT


REQUIRED_SECTIONS = {
    "business_requirements",
    "functional_requirements",
    "non_functional_requirements",
    "business_rules",
    "user_stories",
    "acceptance_criteria",
    "use_cases",
    "risks",
    "assumptions",
    "open_questions",
}


def validate(
    requirements: dict,
    discovery_memory: dict,
) -> dict:
    """
    Validates extracted requirements against discovery memory.

    Validation has two layers:

    1. LLM semantic audit
       - traceability
       - unsupported facts
       - contradictions
       - completeness

    2. Deterministic structural validation
       - required sections
       - forbidden top-level sections
       - response integrity

    Output:
        {
            "valid": bool,
            "issues": [],
            "warnings": [],
            "missing_sections": []
        }
    """

    # --------------------------------------------------
    # Step 1
    # Structural validation of generated document
    # --------------------------------------------------

    issues = []
    warnings = []
    missing_sections = []

    if not isinstance(requirements, dict):
        return {
            "valid": False,
            "issues": [
                "Generated requirements must be a JSON object."
            ],
            "warnings": [],
            "missing_sections": [],
        }

    # --------------------------------------------------
    # Required sections
    # --------------------------------------------------

    for section in REQUIRED_SECTIONS:
        if section not in requirements:
            missing_sections.append(section)

    # --------------------------------------------------
    # Forbidden top-level sections
    #
    # Discovery constraints remain Discovery information.
    # They are not a separate Requirements artifact.
    # --------------------------------------------------

    forbidden_sections = {
        "constraints",
        "deployment",
        "architecture",
        "technology_decisions",
    }

    for section in forbidden_sections:
        if section in requirements:
            issues.append(
                f"Forbidden top-level requirements section detected: "
                f"{section}"
            )

    # --------------------------------------------------
    # Section type validation
    # --------------------------------------------------

    for section in REQUIRED_SECTIONS:
        if section not in requirements:
            continue

        value = requirements[section]

        if not isinstance(value, list):
            issues.append(
                f"Requirements section '{section}' must be a list."
            )

    # --------------------------------------------------
    # Step 2
    # LLM semantic validation
    # --------------------------------------------------

    prompt = f"""
Discovery Memory:

{json.dumps(discovery_memory, indent=2)}

Generated Requirements:

{json.dumps(requirements, indent=2)}

Review the generated requirements against the discovery memory.

Determine whether the requirements are:

- traceable to discovery
- internally consistent
- sufficiently complete for architecture generation
- free from invented project facts
- free from unsupported assumptions
- free from invented workflows
- free from invented integrations
- free from invented technologies
- free from invented user roles
- free from invented numerical targets

Pay particular attention to the distinction between:

1. Information explicitly present in Discovery.
2. Information that is a reasonable interpretation of Discovery.
3. Information that has been invented by the Requirements Agent.

Only category 1 and defensible category 2 information should be accepted.

Category 3 must be reported as an ISSUE.

Do not report optional omissions as issues.

Produce the validation report.
"""

    gateway = LLMGateway()

    content = gateway.generate(
        system_prompt=VALIDATOR_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    report = json.loads(content)

    # --------------------------------------------------
    # Step 3
    # Normalize validator response
    # --------------------------------------------------

    if not isinstance(report, dict):
        report = {}

    report_issues = report.get("issues", [])
    report_warnings = report.get("warnings", [])
    report_missing_sections = report.get(
        "missing_sections",
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

    # --------------------------------------------------
    # Step 4
    # Merge deterministic validation with LLM validation
    # --------------------------------------------------

    issues.extend(report_issues)
    warnings.extend(report_warnings)

    # Avoid duplicate missing section names.
    combined_missing_sections = list(
        dict.fromkeys(
            missing_sections + report_missing_sections
        )
    )

    # --------------------------------------------------
    # Step 5
    # Final validity decision
    #
    # The LLM does not get the final word.
    # Any structural issue or semantic issue means invalid.
    # --------------------------------------------------

    valid = len(issues) == 0

    return {
        "valid": valid,
        "issues": issues,
        "warnings": warnings,
        "missing_sections": combined_missing_sections,
    }