from app.services.report_engine.blocks import (
    BulletListBlock,
    CodeBlock,
    HeadingBlock,
    HorizontalRuleBlock,
    ImageBlock,
    NumberedListBlock,
    ParagraphBlock,
    QuoteBlock,
    TableBlock,
)
from app.services.report_engine.tokenizer import tokenize


def _looks_like_tree_lines(lines: list[str]) -> bool:
    """
    Detect ASCII folder trees / directory listings that were
    emitted as plain text instead of fenced code blocks.
    """
    if not lines:
        return False

    tree_chars = set("├└│─┌┐┬┼┤┘╔╗╚╝║═")
    joined = "\n".join(lines)

    # Strong signal: box-drawing characters
    if any(c in joined for c in tree_chars):
        return True

    # Multiple lines that look like paths / indented hierarchy
    indented = sum(1 for ln in lines if ln.startswith(" ") or ln.startswith("\t"))
    slash_count = joined.count("/")

    if len(lines) >= 2 and indented >= 1 and slash_count >= 2:
        return True

    # Common LLM patterns
    if "..." in joined and any(k in joined.lower() for k in ("layout", "structure", "folder", "directory")):
        return True

    return False


def parse_markdown(markdown: str):
    """
    Parse markdown into structured report blocks.
    """
    tokens = tokenize(markdown)
    blocks = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # -----------------------------
        # Heading
        # -----------------------------
        if token.type == "heading":
            level = len(token.value) - len(token.value.lstrip("#"))
            text = token.value[level:].strip()
            blocks.append(HeadingBlock(level=level, text=text))
            i += 1
            continue

        # -----------------------------
        # Paragraph / possible tree
        # -----------------------------
        if token.type == "text":
            lines = [token.value]
            i += 1

            while i < len(tokens) and tokens[i].type == "text":
                lines.append(tokens[i].value)
                i += 1

            # Key fix: if these consecutive text lines look like
            # a folder tree, emit a CodeBlock instead of a paragraph
            if _looks_like_tree_lines(lines):
                blocks.append(
                    CodeBlock(
                        language="",
                        code="\n".join(lines),
                    )
                )
            else:
                # Normal paragraph – join with space
                blocks.append(
                    ParagraphBlock(text=" ".join(line.strip() for line in lines))
                )
            continue

        # -----------------------------
        # Bullet List
        # -----------------------------
        if token.type == "bullet":
            items = []
            while i < len(tokens) and tokens[i].type == "bullet":
                # Remove leading "- " or "* "
                item = tokens[i].value.lstrip("-* ").strip()
                items.append(item)
                i += 1
            blocks.append(BulletListBlock(items))
            continue

        # -----------------------------
        # Numbered List
        # -----------------------------
        if token.type == "number":
            items = []
            while i < len(tokens) and tokens[i].type == "number":
                value = tokens[i].value
                # Split after the first ". "
                item = value.split(". ", 1)[1].strip() if ". " in value else value
                items.append(item)
                i += 1
            blocks.append(NumberedListBlock(items))
            continue

        # -----------------------------
        # Quote
        # -----------------------------
        if token.type == "quote":
            blocks.append(QuoteBlock(token.value.lstrip("> ").strip()))
            i += 1
            continue

        # -----------------------------
        # Horizontal Rule
        # -----------------------------
        if token.type == "hr":
            blocks.append(HorizontalRuleBlock())
            i += 1
            continue

        # -----------------------------
        # Code Block (fenced)
        # -----------------------------
        if token.type == "code_fence":
            language = token.value.replace("```", "").strip()
            i += 1
            code_lines = []

            while i < len(tokens) and tokens[i].type != "code_fence":
                if tokens[i].type == "code":
                    code_lines.append(tokens[i].value)
                i += 1

            # Skip closing fence
            if i < len(tokens) and tokens[i].type == "code_fence":
                i += 1

            blocks.append(
                CodeBlock(
                    language=language,
                    code="\n".join(code_lines),
                )
            )
            continue

        # -----------------------------
        # Table
        # -----------------------------
        if token.type == "table":
            table_lines = []
            while i < len(tokens) and tokens[i].type == "table":
                table_lines.append(tokens[i].value)
                i += 1

            if len(table_lines) >= 2:
                headers = [x.strip() for x in table_lines[0].strip("|").split("|")]
                rows = []
                for row in table_lines[2:]:
                    rows.append([x.strip() for x in row.strip("|").split("|")])
                blocks.append(TableBlock(headers=headers, rows=rows))
            continue

        # -----------------------------
        # Image
        # -----------------------------
        if token.type == "image":
            value = token.value
            try:
                alt = value.split("[", 1)[1].split("]", 1)[0]
                path = value.split("(", 1)[1].split(")", 1)[0]
                blocks.append(ImageBlock(alt=alt, path=path))
            except (IndexError, ValueError):
                pass
            i += 1
            continue

        # Skip unknown / blank tokens
        i += 1

    return blocks