import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("tag", "value", None, {"href":"https://www.boot.dev","target":"_blank"})

        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')
    
    def test_values(self):
        node = HTMLNode("div","Brian Asplode")

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Brian Asplode")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("tag","value",None,{"href":"https://AUGGHHH"})
        self.assertEqual(node.__repr__(), "HTMLNode(tag, value, children: None, {'href': 'https://AUGGHHH'})")

    def test_to_html_leaf(self):
        node = LeafNode("p","This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
    
    def test_to_html_leaf_props(self):
        node = LeafNode("a","Link here",{"href":"www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Link here</a>')
    
    def test_to_html_leaf_no_tag(self):
        node = LeafNode(None, "Raw Text!")
        self.assertEqual(node.to_html(), "Raw Text!")

if __name__ == "__main__":
    unittest.main()
