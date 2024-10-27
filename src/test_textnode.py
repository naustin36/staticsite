import unittest

from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node,
)

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
        node = TextNode("This has a url", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This has a url", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Text node", TextType.TEXT, "https://www.google.com")
        self.assertEqual(repr(node), "TextNode(Text node, text, https://www.google.com)")
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("normal text", TextType.TEXT)
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, None)
        self.assertEqual(HTML_node.value, "normal text")

    def test_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, "b")
        self.assertEqual(HTML_node.value, "bold text")

    def test_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, "i")
        self.assertEqual(HTML_node.value, "italic text")

    def test_code(self):
        text_node = TextNode("test = yes", TextType.CODE)
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, "code")
        self.assertEqual(HTML_node.value, "test = yes")

    def test_link(self):
        text_node = TextNode("click here", TextType.LINK, "www.google.com")
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, "a")
        self.assertEqual(HTML_node.value, "click here")
        self.assertEqual(HTML_node.props, {"href":"www.google.com"})

    def test_img(self):
        text_node = TextNode("image", TextType.IMAGE, "src/photo.jpg")
        HTML_node = text_node_to_html_node(text_node)
        self.assertEqual(HTML_node.tag, "img")
        self.assertEqual(HTML_node.value, "")
        self.assertEqual(HTML_node.props, {"src":"src/photo.jpg", "alt":"image"})


if __name__ == "__main__":
    unittest.main()
