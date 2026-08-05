from app.agents.architecture.prompt_standards import PROMPT_STANDARD


SYSTEM_PROMPT = """
You are ArchitectAI's Principal Enterprise Solutions Architect.

You have over 20 years of experience designing enterprise software systems for governments, hospitals, banks, insurance companies, Fortune 500 organizations, and global technology firms.

You are responsible for generating ONE section of a Software Architecture Document (SAD).

The Architecture Orchestrator will combine your output with other independently generated sections.

Always follow enterprise architecture best practices.

Return valid Markdown only.
"""


EXECUTIVE_SUMMARY_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Executive Summary

PURPOSE

Provide a concise executive overview of the proposed solution.

REQUIRED HEADINGS

## Business Overview

## Business Objectives

## Proposed Solution

## Expected Business Outcomes

## Architecture Style

## Key Benefits

REQUIRED TABLE

| Business Goal | Expected Outcome |

EXCLUSIONS

Do not discuss deployment.

Do not discuss databases.

Do not discuss APIs.

Generate ONLY this section.
"""


BUSINESS_CONTEXT_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Business Context

PURPOSE

Describe the business environment, stakeholders, drivers and project scope.

REQUIRED HEADINGS

## Business Challenges

## Business Drivers

## Stakeholders

## Primary Users

## Secondary Users

## Project Scope

## Out of Scope

REQUIRED TABLE

| Stakeholder | Responsibility |

EXCLUSIONS

Do not discuss technical implementation.

Generate ONLY this section.
"""


FUNCTIONAL_ARCHITECTURE_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Functional Architecture

PURPOSE

Describe the major functional capabilities of the solution.

REQUIRED HEADINGS

## Functional Overview

## Major Modules

## Responsibilities

## User Workflows

## Business Processes

## Service Interactions

REQUIRED TABLE

| Module | Responsibility |

EXCLUSIONS

Do not discuss deployment.

Generate ONLY this section.
"""


DATA_ARCHITECTURE_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Data Architecture

PURPOSE

Describe how data is stored, managed and governed.

REQUIRED HEADINGS

## Data Overview

## Core Entities

## Data Lifecycle

## Storage Strategy

## Data Integration

## Data Security

## Backup Strategy

REQUIRED TABLE

| Entity | Description |

EXCLUSIONS

Do not generate SQL.

Do not discuss APIs.

Generate ONLY this section.
"""


API_ARCHITECTURE_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

API Architecture

PURPOSE

Describe the API strategy and integration approach.

REQUIRED HEADINGS

## API Style

## Authentication

## Authorization

## Versioning

## Error Handling

## Rate Limiting

## External Integrations

REQUIRED TABLE

| API | Purpose |

EXCLUSIONS

Do not discuss deployment.

Generate ONLY this section.
"""


AI_ARCHITECTURE_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

AI Architecture

PURPOSE

Describe the AI capabilities and workflow.

REQUIRED HEADINGS

## AI Objectives

## AI Components

## Models

## Embedding Strategy

## Retrieval Strategy

## Prompt Engineering

## AI Monitoring

## Human Oversight

REQUIRED TABLE

| AI Component | Responsibility |

EXCLUSIONS

Only include this section if AI is part of the solution.

Generate ONLY this section.
"""


SECURITY_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Security Architecture

PURPOSE

Describe how the platform is secured.

REQUIRED HEADINGS

## Authentication

## Authorization

## Encryption

## Secrets Management

## Audit Logging

## Compliance

## Threat Mitigation

## Security Risks

REQUIRED TABLES

| Security Decision | Reason | Trade-off |

| Risk | Impact | Mitigation |

EXCLUSIONS

Do not discuss deployment.

Generate ONLY this section.
"""


DEPLOYMENT_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Deployment Architecture

PURPOSE

Describe the production deployment strategy.

REQUIRED HEADINGS

## Deployment Model

## Infrastructure

## Network Topology

## Load Balancing

## High Availability

## Auto Scaling

## Disaster Recovery

## Monitoring

## Logging

REQUIRED TABLE

| Deployment Decision | Reason |

EXCLUSIONS

Do not discuss APIs.

Generate ONLY this section.
"""


DEVOPS_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

DevOps Architecture

PURPOSE

Describe operational processes for delivering and maintaining the platform.

REQUIRED HEADINGS

## CI/CD Pipeline

## Release Strategy

## Rollback Strategy

## Infrastructure as Code

## Monitoring

## Alerting

## Logging

## Operational Metrics

REQUIRED TABLE

| Process | Tool | Purpose |

EXCLUSIONS

Do not discuss business requirements.

Generate ONLY this section.
"""


TECHNOLOGY_DECISIONS_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Technology Decisions

PURPOSE

Explain the rationale behind major technology selections.

REQUIRED HEADINGS

## Technology Stack

## Decision Criteria

## Alternatives Considered

## Trade-offs

## Risks

REQUIRED TABLE

| Technology | Reason | Trade-off |

EXCLUSIONS

Do not repeat previous architecture sections.

Generate ONLY this section.
"""


RISKS_PROMPT = f"""
{PROMPT_STANDARD}

SECTION

Risks and Mitigations

PURPOSE

Identify the key project risks and how they should be mitigated.

REQUIRED HEADINGS

## Technical Risks

## Security Risks

## Operational Risks

## Business Risks

## AI Risks

## Mitigation Strategy

REQUIRED TABLE

| Risk | Probability | Impact | Mitigation |

EXCLUSIONS

Do not generate recommendations outside this section.

Generate ONLY this section.
"""