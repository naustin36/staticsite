import unittest

from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images, 
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type
)

from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_single(self):
        node = TextNode("This has a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has a ", TextType.TEXT, None),
                TextNode("bold", TextType.BOLD, None), 
                TextNode(" word", TextType.TEXT, None)]
        )
    
    def test_split_nodes_delimiter_list(self):
        nodes = [TextNode("This has an *italics* word", TextType.TEXT), TextNode("This has another *italics* word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("This has another ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_invalid_markdown(self):
        node = TextNode("This **bold word is broke", TextType.TEXT)
        try:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        except Exception as e:
            print(e)

    def test_split_nodes_delimiter_non_text(self):
        nodes = [TextNode("BOLD WORDS", TextType.BOLD), TextNode("This has a **bold** word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("BOLD WORDS", TextType.BOLD),
                TextNode("This has a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_multiple_occurance(self):
        node = TextNode("This has **two** bold **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("words", TextType.BOLD)
            ]
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("This has **bold** and also *italic* words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and also ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" words", TextType.TEXT)
            ]
        )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_tuples = extract_markdown_images(text)
        self.assertListEqual(
            image_tuples,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
    
    def test_extract_images_with_link(self):
        text = "This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        image_tuples = extract_markdown_images(text)
        self.assertListEqual(
            image_tuples,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        )

    def test_extract_images_without_image(self):
        text = "There are no links here"
        image_tuples = extract_markdown_images(text)
        self.assertListEqual(
            image_tuples,
            []
        )

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_tuples = extract_markdown_links(text)
        self.assertListEqual(
            link_tuples,
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extract_links_with_image(self):
        text = "This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        link_tuples = extract_markdown_links(text)
        self.assertListEqual(
            link_tuples,
            [("to boot dev", "https://www.boot.dev")]
        )

    def test_split_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )
    
    def test_split_images2(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) Plus a little extra", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" Plus a little extra", TextType.TEXT)
            ]
        )

    def test_split_images_with_links(self):
        node = TextNode("This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This text has an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
            ]
        )

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) Plus a little extra", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" Plus a little extra", TextType.TEXT)
            ]
        )
    
    def test_split_links_with_images(self):
        node = TextNode("This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ]
        )

    def test_split_links_and_images(self):
        node = TextNode("This text has an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This text has an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ]
        )

    def test_markdown_to_block(self):
        markdown = "# This is a heading\n\nThis is a paragraph with **bold** and *italic* words in it.\n\n* This is first\n* This is second\n* This is third"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph with **bold** and *italic* words in it.",
                "* This is first\n* This is second\n* This is third"
            ]
        )

    def test_markdown_to_block_excessive_newlines_and_whitespace(self):
        markdown = "  # This is a heading\n\n\nThis is a paragraph with **bold** and *italic* words in it.   \n\n\n\n* This is first\n* This is second\n* This is third"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph with **bold** and *italic* words in it.",
                "* This is first\n* This is second\n* This is third"
            ]
        )

    def test_markdown_to_block_oneblock(self):
        markdown = "# This is a heading"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading"
            ]
        )

    def test_block_type(self):
        heading_block = block_to_block_type("# This is a heading")
        code_block = block_to_block_type("```This is code```")
        quote_block = block_to_block_type(">This is\n>a quote")
        unordered_list_block1 = block_to_block_type("* This is an\n* unordered list")
        unordered_list_block2 = block_to_block_type("- This is another\n- unordered list")
        ordered_list_block = block_to_block_type("1. This is an\n2. ordered list\n3. that has\n4. four items")
        paragraph_block = block_to_block_type("This is a paragraph")
        messed_up_block = block_to_block_type("``This isn't code and should be a paragraph``")
        mixed_list = block_to_block_type("* This is\n- a mixed bullet\n* list and is bad")

        self.assertEqual(heading_block, "heading")
        self.assertEqual(code_block, "code")
        self.assertEqual(quote_block, "quote")
        self.assertEqual(unordered_list_block1, "unordered_list")
        self.assertEqual(unordered_list_block2, "unordered_list")
        self.assertEqual(ordered_list_block, "ordered_list")
        self.assertEqual(paragraph_block, "paragraph")
        self.assertEqual(messed_up_block, "paragraph")
        self.assertEqual(mixed_list, "paragraph")


    def test_block_type_multiline(self):
        code_block = block_to_block_type("```This is a test\nof multiline code```")

        self.assertEqual(code_block, "code")


class TestTextToTextNodes(unittest.TestCase):
    def text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)

        self.assertListEqual(
            text_nodes,
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
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )
    
    def test_to_textnodes2(self):
        text = "Here is a **markdown** string that I'm *trying* to convert into [text nodes](https://www.boot.dev), but it's giving me a ![migraine](https://www.headache.ick/migraine.jpg) I *just* wanna **win!**"
        text_nodes = text_to_textnodes(text)

        self.assertListEqual(
            text_nodes,
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("markdown", TextType.BOLD),
                TextNode(" string that I'm ", TextType.TEXT),
                TextNode("trying", TextType.ITALIC),
                TextNode(" to convert into ", TextType.TEXT),
                TextNode("text nodes", TextType.LINK, "https://www.boot.dev"),
                TextNode(", but it's giving me a ", TextType.TEXT),
                TextNode("migraine", TextType.IMAGE, "https://www.headache.ick/migraine.jpg"),
                TextNode(" I ", TextType.TEXT),
                TextNode("just", TextType.ITALIC),
                TextNode(" wanna ", TextType.TEXT),
                TextNode("win!", TextType.BOLD)
            ]
        )

if __name__ == "__main__":
    unittest.main()