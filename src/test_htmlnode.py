import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("p", "hello", None, { "href": "https://www.google.com", "target": "_blank" })
        node2 = HTMLNode("p", "hello", None, { "href": "https://www.google.com", "type": "input", "target": "_blank" })
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.google.com\" type=\"input\" target=\"_blank\"")

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()