from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


def tokenize(markdown: str) -> list[Token]:
    tokens = []
    lines = markdown.splitlines()
    in_code = False

    for line in lines:
        # Keep trailing whitespace removal only
        raw = line.rstrip("\n")
        stripped = raw.strip()

        # -----------------------------
        # Code fences
        # -----------------------------
        if stripped.startswith("```"):
            tokens.append(Token("code_fence", stripped))
            in_code = not in_code
            continue

        # -----------------------------
        # Everything inside a code block stays as code
        # (preserve exact original line including indentation)
        # -----------------------------
        if in_code:
            tokens.append(Token("code", raw))
            continue

        # -----------------------------
        # Blank line
        # -----------------------------
        if stripped == "":
            tokens.append(Token("blank", ""))
            continue

        # -----------------------------
        # Heading
        # -----------------------------
        if stripped.startswith("#"):
            tokens.append(Token("heading", stripped))
            continue

        # -----------------------------
        # Quote
        # -----------------------------
        if stripped.startswith(">"):
            tokens.append(Token("quote", stripped))
            continue

        # -----------------------------
        # Bullet
        # -----------------------------
        if stripped.startswith("- ") or stripped.startswith("* "):
            tokens.append(Token("bullet", stripped))
            continue

        # -----------------------------
        # Numbered list (supports 1. 2. 10. etc.)
        # -----------------------------
        if len(stripped) > 2 and stripped[0].isdigit():
            # Find the ". " after the number
            dot_pos = stripped.find(". ")
            if dot_pos > 0 and stripped[:dot_pos].isdigit():
                tokens.append(Token("number", stripped))
                continue

        # -----------------------------
        # Table
        # -----------------------------
        if stripped.startswith("|"):
            tokens.append(Token("table", stripped))
            continue

        # -----------------------------
        # Horizontal rule
        # -----------------------------
        if stripped in ("---", "***", "___"):
            tokens.append(Token("hr", stripped))
            continue

        # -----------------------------
        # Image
        # -----------------------------
        if stripped.startswith("!["):
            tokens.append(Token("image", stripped))
            continue

        # -----------------------------
        # Normal text — PRESERVE leading whitespace
        # (this is the key fix for folder trees)
        # -----------------------------
        tokens.append(Token("text", raw))

    return tokens