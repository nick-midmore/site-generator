from enum import Enum
import re

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.strip().split("\n\n")
    for block in blocks:
        if block:
            lines = block.split("\n")
            cleaned_lines = [line.strip() for line in lines]
            cleaned_block = "\n".join(cleaned_lines)
            new_blocks.append(cleaned_block)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "ul"
    OL = "ol"

def block_to_block_type(markdown):
    code_block = r"^```[\s\S]*```$"
    quote = r"^(>.*(\n|$))+$"
    ul = r"^(- .*(\n|$))+$"
    ol = r"^(\d+\..*(\n|$))+$"
    if markdown[0] == "#":
        return BlockType.HEADING
    elif match(markdown, code_block):
        return BlockType.CODE
    elif match(markdown, quote):
        return BlockType.QUOTE
    elif match(markdown, ul):
        return BlockType.UL
    elif match(markdown, ol):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH


def match(text, regex):
    return bool(re.search(text, regex))