import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from app.config import settings
from app.models.project import Project
from app.services.prompt_builder import build_architecture_prompt

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _clean_markdown(content: str) -> str:
    content = content.strip()

    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
    elif content.startswith("```"):
        content = content[3:].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    lines = content.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)

    if lines and lines[0].startswith("# "):
        lines.pop(0)

    while lines and not lines[0].strip():
        lines.pop(0)

    return "\n".join(lines).strip()


def generate_architecture(project: Project) -> str:
    prompt = build_architecture_prompt(project)

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://architectai.local",
        "X-Title": "ArchitectAI",
    }

    system_prompt = "\n".join([
        "You are a Principal Software Architect.",
        "",
        "Generate a production-grade Software Architecture Document.",
        "",
        "IMPORTANT RULES",
        "",
        "- Return VALID RAW MARKDOWN ONLY.",
        "- DO NOT wrap the entire response inside triple backticks.",
        "- DO NOT output ```markdown",
        "- DO NOT generate a document title (no H1).",
        "- The document MUST start with:",
        "",
        "## Executive Summary",
        "",
        "------------------------------------------------",
        "",
        "Use only these heading levels:",
        "",
        "## Heading",
        "### Subheading",
        "",
        "------------------------------------------------",
        "",
        "FOLDER STRUCTURES",
        "",
        "EVERY folder tree MUST be fenced exactly like this:",
        "",
        "```text",
        "project/",
        "├── app/",
        "│   ├── api/",
        "│   ├── models/",
        "│   └── services/",
        "└── README.md",
        "```",
        "",
        "Never output a folder tree as plain text. Always put it inside a ```text fence.",
        "",
        "------------------------------------------------",
        "",
        "CODE BLOCKS",
        "",
        "Always use fenced code blocks with a language tag when showing code, schemas, or configuration.",
        "",
        "------------------------------------------------",
        "",
        "Keep the document professional, clear, and complete.",
    ])

    payload = {
        "model": settings.MODEL_NAME,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=90,
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return _clean_markdown(content)

    except Timeout:
        raise RuntimeError("OpenRouter request timed out. Please try again.")
    except ConnectionError:
        raise RuntimeError(
            "Could not connect to OpenRouter (network / DNS issue). "
            "Check your internet connection and try again."
        )
    except RequestException as e:
        raise RuntimeError(f"OpenRouter request failed: {str(e)}")
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response format from OpenRouter.")