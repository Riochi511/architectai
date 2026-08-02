import re


def md_to_reportlab(text: str) -> str:
    """
    Convert basic Markdown inline syntax
    into ReportLab-compatible markup.
    """

    # Bold
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text,
    )

    # Italic
    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text,
    )

    # Inline code
    text = re.sub(
        r"`(.*?)`",
        r"<font face='Courier'>\1</font>",
        text,
    )

    return text