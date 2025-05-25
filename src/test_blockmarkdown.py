import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line



    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_heading_single_hash(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        block = "### This is a level 3 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_six_hashes(self):
        block = "###### This is a level 6 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_requires_space(self):
        block = "#No space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block_simple(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_with_language(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_empty(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_incomplete(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        block = ">First line of quote\n>Second line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_with_spaces_after_bracket(self):
        block = "> Quote with space\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_mixed_with_non_quote(self):
        block = ">This is a quote\nThis is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_single_item(self):
        block = "- First item"
        self.assertEqual(block_to_block_type(block), BlockType.UL)
    
    def test_unordered_list_multiple_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UL)
    
    def test_unordered_list_requires_space(self):
        block = "-No space after dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_mixed_with_non_list(self):
        block = "- First item\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.OL)
    
    def test_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.OL)
    
    def test_ordered_list_must_start_with_one(self):
        block = "2. Starting with two\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_must_increment_by_one(self):
        block = "1. First item\n3. Skipped two\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_requires_space_after_dot(self):
        block = "1.No space after dot\n2.Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_mixed_with_non_list(self):
        block = "1. First item\nNot a list item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_simple(self):
        block = "This is just a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nthat don't match any pattern."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_whitespace_only_lines_in_quote(self):
        block = ">First line\n>\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_numbers_in_paragraph(self):
        block = "1 This starts with a number but no dot\n2 Same here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_fake_heading_in_middle(self):
        block = "This is a paragraph\n# This looks like heading but isn't first line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)