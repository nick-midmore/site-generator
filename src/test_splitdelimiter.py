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
    
    # def test_type_code(self):
    #     nodes = split_nodes_delimiter([TextNode("This text has no delimiter", TextType.TEXT)], "`", TextType.CODE)
    #     self.assertEqual(nodes, )


if __name__ == '__main__':
    unittest.main()
