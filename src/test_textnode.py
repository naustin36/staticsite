import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This has a url", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This has a url", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_not_equal(self):
        node = TextNode("This has a url", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This has a url", TextType.BOLD, "https://docs.python.org")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
