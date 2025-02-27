import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click here!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click here!</a>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I have no tag :(")
        self.assertEqual(node.to_html(), "I have no tag :(")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("ul", "")
        self.assertEqual(node.to_html(), "<ul></ul>")
    
