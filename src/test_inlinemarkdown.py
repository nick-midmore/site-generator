import unittest
from inline_markdown import * 
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_images(self):
        matches = extract_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_no_matches(self):
        link_matches = extract_links(
            "Text with no [links] anywhere (https://www.google.com)"
        )
        image_matches = extract_images(
            "Text with ![no] images (https://www.google.com)"
        )

        self.assertEqual(len(link_matches), 0)
        self.assertEqual(len(image_matches), 0)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )