import unittest

from textnode import TextType, TextNode

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


if __name__ == "__main__":
    unittest.main()