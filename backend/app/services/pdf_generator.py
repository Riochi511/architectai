from app.services.report_engine.pdf import generate_report_pdf


def generate_pdf(
    title: str,
    markdown_content: str,
) -> str:
    return generate_report_pdf(
        title,
        markdown_content,
    )