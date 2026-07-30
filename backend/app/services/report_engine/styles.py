from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
)
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)

styles = getSampleStyleSheet()


# ==================================================
# Document Title
# ==================================================
TITLE_STYLE = ParagraphStyle(
    "ArchitectAITitle",
    parent=styles["Title"],
    fontSize=24,
    leading=30,
    textColor=colors.HexColor("#1E3A8A"),
    alignment=TA_CENTER,
    spaceAfter=24,
)


# ==================================================
# Main Headings
# ==================================================
HEADING_STYLE = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    fontSize=18,
    leading=24,
    textColor=colors.HexColor("#2563EB"),
    spaceBefore=20,
    spaceAfter=12,
)


# ==================================================
# Sub Headings
# ==================================================
SUBHEADING_STYLE = ParagraphStyle(
    "SubHeading",
    parent=styles["Heading2"],
    fontSize=15,
    leading=20,
    textColor=colors.HexColor("#374151"),
    spaceBefore=14,
    spaceAfter=8,
)


# ==================================================
# Normal Body Text
# ==================================================
BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontSize=11,
    leading=18,
    textColor=colors.black,
    spaceAfter=8,
)


# ==================================================
# Bullet Lists
# ==================================================
BULLET_STYLE = ParagraphStyle(
    "Bullet",
    parent=styles["BodyText"],
    leftIndent=20,
    bulletIndent=10,
    fontSize=11,
    leading=18,
    spaceAfter=4,
)


# ==================================================
# Code Blocks
# ==================================================
CODE_STYLE = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=9,
    leading=12,
    alignment=TA_LEFT,
    leftIndent=18,
    rightIndent=18,
    backColor=colors.HexColor("#F3F4F6"),
    borderColor=colors.HexColor("#D1D5DB"),
    borderWidth=0.5,
    borderPadding=8,
    spaceBefore=10,
    spaceAfter=10,
)