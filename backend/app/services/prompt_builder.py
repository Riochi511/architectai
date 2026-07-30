from app.models.project import Project


def build_architecture_prompt(project: Project) -> str:
    """
    Converts a Project and its Requirements
    into a structured prompt for the LLM.
    """

    prompt = f"""
You are an expert Software Architect.

Generate a professional software architecture document.

Project Name:
{project.name}

Project Description:
{project.description}

Requirements:

"""

    for requirement in project.requirements:
        prompt += f"""
Title: {requirement.title}
Category: {requirement.category}
Priority: {requirement.priority}

Description:
{requirement.description}

"""

    prompt += """

Generate a professional architecture including:

1. Executive Summary

2. Recommended Architecture Style
   (Monolith, Microservices, Event Driven, etc.)

3. Recommended Tech Stack

4. Database Design

5. API Design

6. Security Strategy

7. Scalability Strategy

8. Deployment Recommendation

9. Folder Structure

10. Risks

11. Future Improvements

Return the answer in clean Markdown.
"""

    return prompt