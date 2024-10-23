import re
from textnode import TextNode, TextType

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