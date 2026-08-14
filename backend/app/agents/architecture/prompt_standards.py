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

Use the exact headings requested by the section prompt.

Do not invent additional top-level headings.

Maintain logical ordering.

--------------------------------------------------
3. REQUIRED CONTENT
--------------------------------------------------

Every heading must include:

• Clear explanations
• Architectural reasoning
• Design decisions where applicable
• Enterprise best practices
• Business justification where relevant

Do not write generic textbook content.

Every paragraph should provide project-specific architectural value.

--------------------------------------------------
4. FROZEN ARCHITECTURE CONSTRAINTS
--------------------------------------------------

The following architectural decisions are IMMUTABLE.

They MUST NOT be replaced, contradicted, or silently reinterpreted.

Architecture Style:
• Modular Monolith

Backend:
• FastAPI

Frontend:
• React + Vite + Tailwind CSS + shadcn/ui

Primary Database:
• PostgreSQL

Vector Database:
• Qdrant

Cache:
• Redis

Object Storage:
• Cloud Storage

AI Integration:
• LLM Gateway

LLM Provider Abstraction:
• OpenRouter

Default LLM:
• DeepSeek via OpenRouter

AI Architecture:
• Model-agnostic

AI Coordination:
• Hybrid Orchestration

The architecture generator MUST preserve these decisions
whenever the relevant architecture section discusses them.

Do not replace PostgreSQL with another database.

Do not replace Qdrant with another vector database.

Do not replace Redis with another cache.

Do not replace FastAPI with another backend framework.

Do not replace React/Vite/Tailwind/shadcn/ui with another frontend stack.

Do not replace the LLM Gateway or OpenRouter abstraction with direct
model-provider integration.

Do not replace the Modular Monolith with Microservices.

Do not introduce a competing technology that contradicts a frozen decision.

--------------------------------------------------
5. PROVIDER-AGNOSTIC ARCHITECTURE
--------------------------------------------------

The architecture MUST remain cloud-provider agnostic unless the
project context explicitly specifies a cloud provider.

Use provider-neutral terminology such as:

• Cloud Storage
• Managed PostgreSQL
• Managed Redis
• Container Runtime
• Container Orchestration
• Secrets Management Service
• Monitoring and Observability Platform
• Identity Provider

Do NOT invent or mandate:

• Microsoft Azure
• AWS
• Google Cloud
• Azure Kubernetes Service
• Amazon RDS
• Google Cloud SQL
• Azure Blob Storage
• Azure Monitor
• Application Insights
• Azure Key Vault
• Azure Active Directory
• Azure Machine Learning
• AWS SageMaker
• Amazon S3
• Google Vertex AI

unless the supplied project context explicitly requires that provider
or technology.

If a provider-specific implementation is useful, it MUST be clearly
identified as an optional implementation example and MUST NOT become
a frozen architectural decision.

For example:

"Cloud Storage may be implemented using a provider-specific object
storage service during deployment."

Do not write:

"Azure Blob Storage will be used."

--------------------------------------------------
6. PROJECT FACT DISCIPLINE
--------------------------------------------------

NEVER invent project facts.

Only state a business or technical fact as definite when it is supported
by the supplied project context, requirements, discovery information,
or frozen architectural decisions.

Do NOT invent:

• Business targets
• Percentage improvements
• Revenue figures
• Cost savings
• User counts
• Concurrent-user targets
• Availability targets
• SLA values
• RTO values
• RPO values
• Geographic regions
• Project timelines
• Regulatory obligations
• Named stakeholders
• User roles
• External integrations
• Healthcare standards
• Data retention periods
• Performance targets
• Capacity targets

unless they are explicitly present in the supplied project context.

Never convert a reasonable enterprise assumption into a project fact.

If important information is missing, create an Assumptions section and
clearly label the information as an assumption.

--------------------------------------------------
7. TRACEABILITY
--------------------------------------------------

Major architectural decisions MUST be traceable to one of:

1. A frozen architectural decision
2. Explicit project requirements
3. A clearly stated architectural assumption

Do not introduce technologies simply because they are common
enterprise choices.

Do not introduce cloud services simply because they are commonly
used in enterprise systems.

Do not introduce numerical targets without source support.

--------------------------------------------------
8. ASSUMPTIONS
--------------------------------------------------

If project information is missing:

Create:

## Assumptions

Clearly identify every assumption.

Never present assumptions as confirmed business requirements.

Use assumptions to fill architectural gaps without inventing facts.

Examples:

• "The architecture assumes the existing hospital systems expose
  integration interfaces."

• "The architecture assumes sufficient historical data is available
  for model training."

Do NOT state these as facts unless the project context confirms them.

--------------------------------------------------
9. DECISION RECORDS
--------------------------------------------------

Where applicable include:

| Decision | Reason | Trade-off |

Explain WHY important architectural choices were made.

Decision records must remain consistent with the frozen architecture.

Do not recommend an alternative that contradicts a frozen decision.

--------------------------------------------------
10. RISKS
--------------------------------------------------

Where applicable include:

## Risks

| Risk | Impact | Mitigation |

Focus on realistic enterprise risks.

Risks must be relevant to the architecture being described.

Do not invent numerical probability or financial impact values unless
supported by the project context.

--------------------------------------------------
11. TABLES
--------------------------------------------------

Prefer Markdown tables whenever they improve readability.

Examples:

Decision Matrix

Technology Matrix

Responsibility Matrix

Risk Matrix

Integration Matrix

Do not create tables merely to increase document length.

--------------------------------------------------
12. DIAGRAM PLACEHOLDERS
--------------------------------------------------

If a diagram would normally appear in this section, insert:

> Diagram Placeholder

Then describe what the diagram should contain.

Do not generate Mermaid or PlantUML unless explicitly requested.

--------------------------------------------------
13. AI ARCHITECTURE RULES
--------------------------------------------------

When AI is part of the solution:

The AI architecture MUST preserve the model-agnostic design.

AI functionality should communicate through the LLM Gateway rather than
directly coupling application logic to a specific LLM provider.

OpenRouter is the provider abstraction layer.

DeepSeek is the default LLM through OpenRouter where an LLM is required.

The architecture MUST allow the underlying model to be replaced without
rewriting application business logic.

Do not hard-code a direct dependency on a specific LLM provider.

Do not present DeepSeek as the only possible model.

Use:

"DeepSeek via OpenRouter as the default model"

rather than:

"DeepSeek is the architecture's only LLM."

AI workflows should follow the Hybrid Orchestration strategy.

Clearly distinguish:

• deterministic business logic
• AI inference
• retrieval
• orchestration
• human oversight

Do not allow an LLM to silently replace deterministic business rules
where deterministic logic is required.

--------------------------------------------------
14. TECHNOLOGY DECISION RULES
--------------------------------------------------

Technology Decisions MUST reflect the frozen architecture.

The canonical technology stack is:

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Frontend | React + Vite + Tailwind CSS + shadcn/ui |
| Primary Database | PostgreSQL |
| Vector Database | Qdrant |
| Cache | Redis |
| Object Storage | Cloud Storage |
| LLM Gateway | OpenRouter |
| Default LLM | DeepSeek via OpenRouter |

Technology decisions must explain why these technologies fit the
project.

Alternatives may be discussed for comparison, but they MUST NOT
replace the frozen technologies.

--------------------------------------------------
15. MODULAR MONOLITH RULES
--------------------------------------------------

The system MUST be described as a Modular Monolith.

Modules should represent clear business or domain boundaries.

Modules may communicate through:

• internal application interfaces
• domain services
• events
• shared infrastructure abstractions

Do not describe the system as a microservices architecture.

Do not describe independently deployed services as the primary
architecture.

Future migration of individual modules to microservices may be discussed
only as a future evolution option, not as the current architecture.

--------------------------------------------------
16. ENTERPRISE QUALITY
--------------------------------------------------

Write like a senior Enterprise Architect.

Avoid filler.

Avoid generic AI language.

Avoid unnecessary complexity.

Do not over-engineer the Version 1 architecture.

Prefer the simplest architecture that satisfies the known requirements.

Every architectural decision should have a reason.

Every major technology should have traceability.

--------------------------------------------------
17. OUTPUT
--------------------------------------------------

Return VALID Markdown only.

Never generate another architecture section.

Never wrap the output inside triple backticks.

Never produce an H1 document title.

Generate ONLY the requested architecture section.
"""