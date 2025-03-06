import unittest
from extract import *

class TestExtractFunctions(unittest.TestCase):
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