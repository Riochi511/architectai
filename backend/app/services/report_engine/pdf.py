from pathlib import Path

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.services.report_engine.parser import parse_markdown
from app.services.report_engine.renderer import render_blocks
from app.services.report_engine.styles import get_styles

OUTPUT_DIR = Path("generated_reports")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_report_pdf(
    title: str,
    markdown_content: str,
) -> str:
    """
    Generate a professional PDF report from Markdown.
    """

    styles = get_styles()

    blocks = parse_markdown(markdown_content)

    print(blocks)

    story = []

    # Cover title
    story.append(
        Paragraph(
            title,
            styles["Title"],
        )
    )

    story.append(Spacer(1, 24))

    # Render parsed markdown
    story.extend(
        render_blocks(blocks)
    )

    safe_name = (
        title.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    pdf_path = OUTPUT_DIR / f"{safe_name}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path)
    )

    doc.build(story)

    return str(pdf_path)