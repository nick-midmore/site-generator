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