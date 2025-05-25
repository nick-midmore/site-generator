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

def block_to_block_type(block):
    if is_code(block):
        return BlockType.CODE
    elif is_unordered_list(block):
        return BlockType.UL
    elif is_ordered_list(block):
        return BlockType.OL
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_heading(block):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH

def is_code(block):
    lines = block.split("\n")
    if lines[0][:3] == "```" and lines[-1][-3:] == "```":
        return True
    return False

def is_heading(block):
    pattern = r"^#{1,6} "
    lines = block.split("\n")
    if re.search(pattern, lines[0]) == None:
        return False
    return True

def is_quote(block):
    lines = block.split("\n")
    for line in lines:
        if line[0] != ">":
            return False
    return True

def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if line[:2] != "- ":
            return False
    return True

def is_ordered_list(block):
    lines = block.split("\n")
    counter = 1
    for line in lines:
        pattern = r"^" + str(counter) + r"\. "
        if re.search(pattern, line) == None:
            return False
        counter += 1
    return True