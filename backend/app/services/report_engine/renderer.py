from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

from app.services.report_engine.blocks import (
    BulletListBlock,
    CodeBlock,
    HeadingBlock,
    HorizontalRuleBlock,
    NumberedListBlock,
    ParagraphBlock,
    QuoteBlock,
    TableBlock,
)
from app.services.report_engine.styles import get_styles
from app.services.report_engine.inline import md_to_reportlab


def looks_like_ascii_tree(text: str) -> bool:
    """
    Safety-net detector for any remaining tree-like content
    that slipped through as a ParagraphBlock.
    """
    tree_chars = "├└│─┌┐┬┼┤┘╔╗╚╝║═"
    if any(c in text for c in tree_chars):
        return True
    if text.count("/") >= 3 and ("\n" in text or text.count("  ") >= 2):
        return True
    return False


def render_blocks(blocks):
    styles = get_styles()
    story = []

    for block in blocks:

        # -----------------------------------
        # Headings
        # -----------------------------------
        if isinstance(block, HeadingBlock):
            if block.level == 1:
                style = styles["Title"]
            elif block.level == 2:
                style = styles["Heading2"]
            else:
                style = styles["Heading3"]

            story.append(Paragraph(md_to_reportlab(block.text), style))
            story.append(Spacer(1, 10))

        # -----------------------------------
        # Paragraph (with tree safety net)
        # -----------------------------------
        elif isinstance(block, ParagraphBlock):
            if looks_like_ascii_tree(block.text):
                story.append(Preformatted(block.text, styles["Code"]))
            else:
                story.append(Paragraph(md_to_reportlab(block.text), styles["Body"]))
            story.append(Spacer(1, 8))

        # -----------------------------------
        # Bullet List
        # -----------------------------------
        elif isinstance(block, BulletListBlock):
            items = [
                ListItem(Paragraph(md_to_reportlab(item), styles["Body"]))
                for item in block.items
            ]
            story.append(ListFlowable(items, bulletType="bullet"))
            story.append(Spacer(1, 8))

        # -----------------------------------
        # Numbered List
        # -----------------------------------
        elif isinstance(block, NumberedListBlock):
            items = [
                ListItem(Paragraph(md_to_reportlab(item), styles["Body"]))
                for item in block.items
            ]
            story.append(ListFlowable(items, bulletType="1"))
            story.append(Spacer(1, 8))

        # -----------------------------------
        # Quote
        # -----------------------------------
        elif isinstance(block, QuoteBlock):
            story.append(Paragraph(md_to_reportlab(block.text), styles["Quote"]))
            story.append(Spacer(1, 8))

        # -----------------------------------
        # Code Block  ← always Preformatted
        # -----------------------------------
        elif isinstance(block, CodeBlock):
            # Preserve every space and line exactly
            story.append(Preformatted(block.code, styles["Code"]))
            story.append(Spacer(1, 10))

        # -----------------------------------
        # Table
        # -----------------------------------
        elif isinstance(block, TableBlock):
            data = []
            headers = [
                Paragraph(md_to_reportlab(header), styles["Body"])
                for header in block.headers
            ]
            data.append(headers)

            for row in block.rows:
                data.append([
                    Paragraph(md_to_reportlab(cell), styles["Body"])
                    for cell in row
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1E3A8A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F8FAFC")),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(table)
            story.append(Spacer(1, 12))

        # -----------------------------------
        # Horizontal Rule
        # -----------------------------------
        elif isinstance(block, HorizontalRuleBlock):
            story.append(Spacer(1, 10))

    return story