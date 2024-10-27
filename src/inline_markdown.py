import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    text_nodes = []
    original_text = TextNode(text, TextType.TEXT)

    text_nodes = split_nodes_delimiter([original_text], "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Extracts any valid markdown of the type specified from TextNodes with TEXT type, and returns a new list of TextNodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown: missing {delimiter}")
        strings = node.text.split(delimiter)
        for i in range(len(strings)):
            if strings[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(strings[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(strings[i], text_type))
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        text = node.text
        image_tuples = extract_markdown_images(text)

        if len(image_tuples) == 0:
            new_nodes.append(node)
            continue

        for image in image_tuples:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid image markdown")
            text = sections[1]

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        text = node.text
        link_tuples = extract_markdown_links(text)

        if len(link_tuples) == 0:
            new_nodes.append(node)
            continue

        for link in link_tuples:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            text = sections[1]
            
            if len(sections) != 2:
                raise ValueError("Invalid link markdown")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    # Returns a list of tuples. Each tuple contains the alt text and image URL for the extracted images.
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    # Returns a list of tuples. Each tuple contains the anchor text and URL for the extracted links.
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []

    for i in range(len(blocks)):
        if blocks[i] == "":
            continue
        blocks[i] = blocks[i].strip()
        final_blocks.append(blocks[i])
    return final_blocks

def block_to_block_type(block):
    block_lines = block.split("\n")

    def is_quote(block_lines):
        for line in block_lines:
            if not line.startswith(">"):
                return False
        return True

    def is_unordered_list(block_lines):
        if block_lines[0].startswith("* "):
            for line in block_lines:
                if not line.startswith("* "):
                    return False
        elif block_lines[0].startswith("- "):
            for line in block_lines:
                if not line.startswith("- "):
                    return False
        else:
            return False
        return True

    def is_ordered_list(block_lines):
        for i in range(len(block_lines)):
            if block_lines[i][0:3] != f"{i+1}. ":
                return False
        return True

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if is_quote(block_lines):
        return "quote"
    if is_unordered_list(block_lines):
        return "unordered_list"
    if is_ordered_list(block_lines):
        return "ordered_list"
    return "paragraph"    