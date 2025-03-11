import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Test", TextType.ITALIC)
        self.assertEqual(node.text_type.value, "bold")
        self.assertEqual(node2.text_type.value, "italic")

    def test_url(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Test", TextType.BOLD, "https://www.hello.com")
        self.assertEqual(node.url, None)
        self.assertEqual(node2.url, "https://www.hello.com")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()