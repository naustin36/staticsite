import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()
