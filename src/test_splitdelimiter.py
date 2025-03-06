import unittest

from splitdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("This text has no delimiter", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(nodes, [TextNode("This text has no delimiter", TextType.TEXT)])
    
    def test_no_closing_delimiter(self):
        with self.assertRaises(Exception) as context:
            nodes = split_nodes_delimiter([TextNode("This text has no `closing delimiter", TextType.TEXT)], "`", TextType.CODE)
        
        self.assertTrue("No closing delimiter found - invalid markdown" in str(context.exception))
    
    def test_type_code(self):
        nodes = split_nodes_delimiter([TextNode("This text has a `code block` in it", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(nodes, [
            TextNode("This text has a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it", TextType.TEXT)
        ])

    def test_type_bold(self):
        nodes = split_nodes_delimiter([TextNode("This text has a **bold** word", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("This text has a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ])
    
    def test_delimiter_at_start(self):
        nodes = split_nodes_delimiter([TextNode("**This text is bold** and this is not", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("This text is bold", TextType.BOLD),
            TextNode(" and this is not", TextType.TEXT)
        ])

    def test_delimiter_at_end(self):
        nodes = split_nodes_delimiter([TextNode("Normal and **bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("Normal and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ])

    def test_multiple_delimiter_pairs(self):
        nodes = split_nodes_delimiter([TextNode("Normal and **bold** and normal **and bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("Normal and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and normal ", TextType.TEXT),
            TextNode("and bold", TextType.BOLD)
        ])

if __name__ == '__main__':
    unittest.main()
