SECTION_ORDER = [
    "executive_summary",
    "business_context",
    "functional_architecture",
    "data_architecture",
    "api_architecture",
    "ai_architecture",
    "security",
    "deployment",
    "devops",
    "technology_decisions",
    "risks",
]


class ArchitectureCompiler:
    """
    Compiles independently generated architecture
    sections into a single Software Architecture
    Document.
    """

    def compile(self, sections: dict[str, str]) -> str:
        document = []

        for section in SECTION_ORDER:

            content = sections.get(section)

            if content:
                document.append(content.strip())

        return "\n\n".join(document)