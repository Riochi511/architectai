from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# backend/app
BASE_DIR = Path(__file__).resolve().parents[2]

# backend/app/fonts
FONT_DIR = BASE_DIR / "fonts"

# Register fonts once
try:
    pdfmetrics.getFont("DejaVuSans")
except KeyError:
    pdfmetrics.registerFont(
        TTFont("DejaVuSans", str(FONT_DIR / "DejaVuSans.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("DejaVuSans-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
    )
    # Monospace font for code blocks & folder trees
    pdfmetrics.registerFont(
        TTFont("DejaVuSansMono", str(FONT_DIR / "DejaVuSansMono.ttf"))
    )


def get_styles():
    """
    Professional ArchitectAI PDF styles.
    """
    base = getSampleStyleSheet()
    styles = {}

    styles["Title"] = ParagraphStyle(
        "Title",
        parent=base["Title"],
        fontName="DejaVuSans-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=24,
    )

    styles["Heading1"] = ParagraphStyle(
        "Heading1",
        parent=base["Heading1"],
        fontName="DejaVuSans-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=18,
        spaceAfter=10,
    )

    styles["Heading2"] = ParagraphStyle(
        "Heading2",
        parent=base["Heading2"],
        fontName="DejaVuSans-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=16,
        spaceAfter=8,
    )

    styles["Heading3"] = ParagraphStyle(
        "Heading3",
        parent=base["Heading3"],
        fontName="DejaVuSans-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=12,
        spaceAfter=6,
    )

    styles["Body"] = ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName="DejaVuSans",
        fontSize=11,
        leading=18,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )

    styles["Quote"] = ParagraphStyle(
        "Quote",
        parent=styles["Body"],
        fontName="DejaVuSans",
        leftIndent=20,
        rightIndent=20,
        textColor=colors.HexColor("#475569"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderPadding=8,
        borderWidth=1,
        borderLeft=True,
        italic=True,
        spaceBefore=8,
        spaceAfter=8,
    )

    # ← This is the important change
    styles["Code"] = ParagraphStyle(
        "Code",
        parent=base["Code"],
        fontName="DejaVuSansMono",      # Unicode monospace font
        fontSize=9,
        leading=13,
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=1,
        borderPadding=8,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=8,
        spaceAfter=8,
    )

    return styles