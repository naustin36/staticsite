import unittest
from html_blocks import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph_block(self):
        markdown = "This is just a paragraph"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><p>This is just a paragraph</p></div>")
    
    def test_heading_block(self):
        h1 = "# This is heading 1"
        h2 = "## This is heading 2"
        h3 = "### This is heading 3"
        h4 = "#### This is heading 4"
        h5 = "##### This is heading 5"
        h6 = "###### This is heading 6"

        h1_node = markdown_to_html_node(h1)
        h2_node = markdown_to_html_node(h2)
        h3_node = markdown_to_html_node(h3)
        h4_node = markdown_to_html_node(h4)
        h5_node = markdown_to_html_node(h5)
        h6_node = markdown_to_html_node(h6)

        self.assertEqual(h1_node.to_html(), "<div><h1>This is heading 1</h1></div>")
        self.assertEqual(h2_node.to_html(), "<div><h2>This is heading 2</h2></div>")
        self.assertEqual(h3_node.to_html(), "<div><h3>This is heading 3</h3></div>")
        self.assertEqual(h4_node.to_html(), "<div><h4>This is heading 4</h4></div>")
        self.assertEqual(h5_node.to_html(), "<div><h5>This is heading 5</h5></div>")
        self.assertEqual(h6_node.to_html(), "<div><h6>This is heading 6</h6></div>")

    def test_paragraph_and_heading(self):
        markdown = "# This is a heading\n\nAnd this is a paragraph"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>This is a heading</h1><p>And this is a paragraph</p></div>")
    
    def test_code_block(self):
        markdown = "```This is code: x=1```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><pre><code>This is code: x=1</code></pre></div>")

    def test_quote_block(self):
        markdown = ">This is\n>a quote"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><blockquote>This is\na quote</blockquote></div>")

    def test_list_blocks(self):
        ul = "* This is\n* An unordered\n* List"
        ol = "1. This is\n2. An ordered\n3. List"
        ul_node = markdown_to_html_node(ul)
        ol_node = markdown_to_html_node(ol)
        self.assertEqual(ul_node.to_html(), "<div><ul><li>This is</li><li>An unordered</li><li>List</li></ul></div>")
        self.assertEqual(ol_node.to_html(), "<div><ol><li>This is</li><li>An ordered</li><li>List</li></ol></div>")
    
    def test_mixed_block(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        )
if __name__ == "__main__":
    unittest.main()
