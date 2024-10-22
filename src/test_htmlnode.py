import unittest

from htmlnode import LeafNode, ParentNode, HTMLNode

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

    def test_to_html_parent(self):
        node = ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "Normal text")
            ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>"
        )
    
    def test_to_html_nested_parents(self):
        node = ParentNode("p", [
            ParentNode("b", [
                LeafNode("i","italics"),
                LeafNode(None,"normal text")
            ]),
            LeafNode("b","bold text"),
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b><i>italics</i>normal text</b><b>bold text</b></p>"
        )
    
    def test_to_html_parent_no_children(self):
        node = ParentNode("p", None)
        try:
            node.to_html()
        except Exception as e:
            print(e)
    
    def test_to_html_parent_props(self):
        node = ParentNode("a", [LeafNode("b", "click")],{"href":"www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="www.google.com"><b>click</b></a>'
        )


if __name__ == "__main__":
    unittest.main()
