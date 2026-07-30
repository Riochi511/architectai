import re
from dataclasses import dataclass


@dataclass
class ReportBlock:
    type: str
    content: str
    level: int = 0


def parse_markdown(markdown: str) -> list[ReportBlock]:
    """
    Parse AI-generated markdown into structured report blocks.
    """

    blocks = []

    lines = markdown.splitlines()

    in_code_block = False
    code_lines = []

    for line in lines:

        line = line.rstrip()

        # -----------------------------
        # Handle fenced code blocks
        # -----------------------------
        if line.strip().startswith("```"):

            if not in_code_block:
                in_code_block = True
                code_lines = []

            else:
                blocks.append(
                    ReportBlock(
                        type="code",
                        content="\n".join(code_lines),
                    )
                )

                in_code_block = False
                code_lines = []

            continue

        if in_code_block:
            code_lines.append(line)
            continue

        line = line.strip()

        if not line:
            continue

        # -----------------------------
        # Title
        # -----------------------------
        if line.startswith("# "):
            blocks.append(
                ReportBlock(
                    type="title",
                    content=line[2:].strip(),
                )
            )

        # -----------------------------
        # Heading
        # -----------------------------
        elif line.startswith("## "):
            blocks.append(
                ReportBlock(
                    type="heading",
                    content=line[3:].strip(),
                )
            )

        # -----------------------------
        # Subheading
        # -----------------------------
        elif line.startswith("### "):
            blocks.append(
                ReportBlock(
                    type="subheading",
                    content=line[4:].strip(),
                )
            )

        # -----------------------------
        # Bullet List
        # -----------------------------
        elif line.startswith("- "):
            blocks.append(
                ReportBlock(
                    type="bullet",
                    content=line[2:].strip(),
                )
            )

        elif line.startswith("* "):
            blocks.append(
                ReportBlock(
                    type="bullet",
                    content=line[2:].strip(),
                )
            )

        # -----------------------------
        # Numbered List
        # -----------------------------
        elif re.match(r"^\d+\.\s", line):

            item = re.sub(
                r"^\d+\.\s*",
                "",
                line,
            )

            blocks.append(
                ReportBlock(
                    type="number",
                    content=item,
                )
            )

        # -----------------------------
        # Paragraph
        # -----------------------------
        else:
            blocks.append(
                ReportBlock(
                    type="paragraph",
                    content=line,
                )
            )

    return blocks