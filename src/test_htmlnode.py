import unittest

from htmlnode import HTMLNode 

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("p", "hello", None, { "href": "https://www.google.com", "target": "_blank" })
        node2 = HTMLNode("p", "hello", None, { "href": "https://www.google.com", "type": "input", "target": "_blank" })
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.google.com\" type=\"input\" target=\"_blank\"")

if __name__ == "__main__":
    unittest.main()