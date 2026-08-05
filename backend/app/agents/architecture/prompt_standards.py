PROMPT_STANDARD = """
Every architecture section MUST follow this structure.

--------------------------------------------------
1. PURPOSE
--------------------------------------------------

Begin by explaining the purpose of the section.

The purpose should be concise and business-focused.

--------------------------------------------------
2. REQUIRED HEADINGS
--------------------------------------------------

Use the exact headings requested.

Do not invent additional top-level headings.

Maintain logical ordering.

--------------------------------------------------
3. REQUIRED CONTENT
--------------------------------------------------

Every heading must include:

• Clear explanations

• Architectural reasoning

• Design decisions

• Enterprise best practices

• Business justification

Do not write generic textbook content.

--------------------------------------------------
4. DECISION RECORDS
--------------------------------------------------

Where applicable include:

| Decision | Reason | Trade-off |

Explain WHY important architectural choices were made.

--------------------------------------------------
5. ASSUMPTIONS
--------------------------------------------------

If project information is missing:

Create an Assumptions section.

Clearly identify every assumption.

Never invent business facts.

--------------------------------------------------
6. RISKS
--------------------------------------------------

Where applicable include:

## Risks

| Risk | Impact | Mitigation |

Focus on realistic enterprise risks.

--------------------------------------------------
7. TABLES
--------------------------------------------------

Prefer Markdown tables whenever they improve readability.

Examples:

Decision Matrix

Technology Matrix

Responsibility Matrix

Risk Matrix

Integration Matrix

--------------------------------------------------
8. DIAGRAM PLACEHOLDERS
--------------------------------------------------

If a diagram would normally appear in this section,

insert:

> Diagram Placeholder

Then describe what the diagram should contain.

Do not generate Mermaid or PlantUML unless explicitly requested.

--------------------------------------------------
9. ENTERPRISE QUALITY
--------------------------------------------------

Write like a senior Enterprise Architect.

Avoid filler.

Avoid generic AI language.

Every paragraph should add value.

--------------------------------------------------
10. OUTPUT
--------------------------------------------------

Return VALID Markdown only.

Never generate another architecture section.

Never wrap inside triple backticks.

Never produce an H1 document title.
"""