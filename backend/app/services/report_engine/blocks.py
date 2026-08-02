from dataclasses import dataclass, field
from typing import List


@dataclass
class Block:
    type: str


@dataclass
class HeadingBlock(Block):
    level: int
    text: str

    def __init__(self, level: int, text: str):
        super().__init__("heading")
        self.level = level
        self.text = text


@dataclass
class ParagraphBlock(Block):
    text: str

    def __init__(self, text: str):
        super().__init__("paragraph")
        self.text = text


@dataclass
class BulletListBlock(Block):
    items: List[str] = field(default_factory=list)

    def __init__(self, items: List[str]):
        super().__init__("bullet_list")
        self.items = items


@dataclass
class NumberedListBlock(Block):
    items: List[str] = field(default_factory=list)

    def __init__(self, items: List[str]):
        super().__init__("numbered_list")
        self.items = items


@dataclass
class QuoteBlock(Block):
    text: str

    def __init__(self, text: str):
        super().__init__("quote")
        self.text = text


@dataclass
class HorizontalRuleBlock(Block):
    def __init__(self):
        super().__init__("horizontal_rule")


@dataclass
class CodeBlock(Block):
    language: str
    code: str

    def __init__(self, language: str, code: str):
        super().__init__("code")
        self.language = language
        self.code = code


@dataclass
class TableBlock(Block):
    headers: List[str]
    rows: List[List[str]]

    def __init__(self, headers: List[str], rows: List[List[str]]):
        super().__init__("table")
        self.headers = headers
        self.rows = rows


@dataclass
class ImageBlock(Block):
    alt: str
    path: str

    def __init__(self, alt: str, path: str):
        super().__init__("image")
        self.alt = alt
        self.path = path