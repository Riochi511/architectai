from reportlab.platypus import Paragraph

from app.services.report_engine.parser import ReportBlock
from app.services.report_engine.styles import (
    TITLE_STYLE,
    HEADING_STYLE,
    SUBHEADING_STYLE,
    BODY_STYLE,
    BULLET_STYLE,
    CODE_STYLE,
)


def render_blocks(
    blocks: list[ReportBlock],
):
    """
    Convert parsed report blocks into ReportLab flowables.
    """

    story = []

    for block in blocks:

        # -----------------------------------
        # Document Title
        # -----------------------------------
        if block.type == "title":
            story.append(
                Paragraph(
                    block.content,
                    TITLE_STYLE,
                )
            )

        # -----------------------------------
        # Heading
        # -----------------------------------
        elif block.type == "heading":
            story.append(
                Paragraph(
                    block.content,
                    HEADING_STYLE,
                )
            )

        # -----------------------------------
        # Sub Heading
        # -----------------------------------
        elif block.type == "subheading":
            story.append(
                Paragraph(
                    block.content,
                    SUBHEADING_STYLE,
                )
            )

        # -----------------------------------
        # Bullet List
        # -----------------------------------
        elif block.type == "bullet":
            story.append(
                Paragraph(
                    f"• {block.content}",
                    BULLET_STYLE,
                )
            )

        # -----------------------------------
        # Numbered List
        # -----------------------------------
        elif block.type == "number":
            story.append(
                Paragraph(
                    f"• {block.content}",
                    BULLET_STYLE,
                )
            )

        # -----------------------------------
        # Code Block
        # -----------------------------------
        elif block.type == "code":

            code = (
                block.content
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>")
                .replace(" ", "&nbsp;")
            )

            story.append(
                Paragraph(
                    code,
                    CODE_STYLE,
                )
            )

        # -----------------------------------
        # Normal Paragraph
        # -----------------------------------
        else:
            story.append(
                Paragraph(
                    block.content,
                    BODY_STYLE,
                )
            )

    return story